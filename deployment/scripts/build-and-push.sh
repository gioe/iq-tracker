#!/bin/bash
set -e

# Build and push Docker images to ECR
# Usage: ./build-and-push.sh [backend|question-service|all]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TERRAFORM_DIR="$REPO_ROOT/deployment/terraform"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Terraform outputs exist
if [ ! -f "$TERRAFORM_DIR/terraform.tfstate" ]; then
    log_error "Terraform state not found. Run 'terraform apply' first."
    exit 1
fi

# Get ECR URLs from Terraform outputs
cd "$TERRAFORM_DIR"
BACKEND_ECR=$(terraform output -raw ecr_backend_repository_url)
QUESTION_SERVICE_ECR=$(terraform output -raw ecr_question_service_repository_url)
AWS_REGION=$(terraform output -raw aws_region 2>/dev/null || echo "us-east-1")
cd -

# Authenticate Docker with ECR
log_info "Authenticating Docker with ECR..."
aws ecr get-login-password --region "$AWS_REGION" | \
    docker login --username AWS --password-stdin "$(echo "$BACKEND_ECR" | cut -d'/' -f1)"
log_success "Docker authenticated with ECR"

build_and_push() {
    local service=$1
    local context_dir=$2
    local ecr_url=$3
    local image_name=$4

    log_info "Building $service image..."
    cd "$REPO_ROOT/$context_dir"
    docker build -t "$image_name" .
    log_success "Built $service image"

    log_info "Tagging $service image..."
    docker tag "$image_name:latest" "$ecr_url:latest"
    docker tag "$image_name:latest" "$ecr_url:$(date +%Y%m%d-%H%M%S)"
    log_success "Tagged $service image"

    log_info "Pushing $service image to ECR..."
    docker push "$ecr_url:latest"
    docker push "$ecr_url:$(date +%Y%m%d-%H%M%S)"
    log_success "Pushed $service image to ECR"
}

# Determine what to build
TARGET="${1:-all}"

case $TARGET in
    backend)
        build_and_push "backend" "backend" "$BACKEND_ECR" "iq-tracker-backend"
        ;;
    question-service)
        build_and_push "question-service" "question-service" "$QUESTION_SERVICE_ECR" "iq-tracker-question-service"
        ;;
    all)
        build_and_push "backend" "backend" "$BACKEND_ECR" "iq-tracker-backend"
        build_and_push "question-service" "question-service" "$QUESTION_SERVICE_ECR" "iq-tracker-question-service"
        ;;
    *)
        log_error "Invalid target: $TARGET"
        echo "Usage: $0 [backend|question-service|all]"
        exit 1
        ;;
esac

log_success "All images built and pushed successfully!"
