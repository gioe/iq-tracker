#!/bin/bash
set -e

# Deploy application to AWS ECS
# Usage: ./deploy.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TERRAFORM_DIR="$REPO_ROOT/deployment/terraform"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Terraform outputs exist
if [ ! -f "$TERRAFORM_DIR/terraform.tfstate" ]; then
    log_error "Terraform state not found. Run 'terraform apply' first."
    exit 1
fi

# Get values from Terraform outputs
cd "$TERRAFORM_DIR"
ECS_CLUSTER=$(terraform output -raw ecs_cluster_name)
ECS_SERVICE=$(terraform output -raw backend_service_name)
AWS_REGION=$(terraform output -raw aws_region 2>/dev/null || echo "us-east-1")
cd -

log_info "Deploying to ECS cluster: $ECS_CLUSTER"
log_info "Service: $ECS_SERVICE"
log_info "Region: $AWS_REGION"

# Build and push images
log_info "Building and pushing Docker images..."
"$SCRIPT_DIR/build-and-push.sh" all

# Force ECS service to redeploy with new images
log_info "Forcing ECS service redeployment..."
aws ecs update-service \
    --cluster "$ECS_CLUSTER" \
    --service "$ECS_SERVICE" \
    --force-new-deployment \
    --region "$AWS_REGION" \
    --output json > /dev/null

log_success "Deployment initiated!"

# Wait for deployment to stabilize
log_info "Waiting for deployment to stabilize (this may take a few minutes)..."
aws ecs wait services-stable \
    --cluster "$ECS_CLUSTER" \
    --services "$ECS_SERVICE" \
    --region "$AWS_REGION"

log_success "Deployment completed successfully!"

# Get ALB DNS and test health endpoint
cd "$TERRAFORM_DIR"
ALB_DNS=$(terraform output -raw alb_dns_name)
cd -

log_info "Testing health endpoint..."
sleep 10 # Give the service a moment to fully start

if curl -sf "http://$ALB_DNS/v1/health" > /dev/null; then
    log_success "Health check passed!"
    log_info "API available at: http://$ALB_DNS"
else
    log_warning "Health check failed. Check CloudWatch logs for details."
    log_info "View logs: aws logs tail /ecs/$ECS_CLUSTER --follow --region $AWS_REGION"
fi
