import SwiftUI

/// A reusable loading indicator view
struct LoadingView: View {
    var message: String = "Loading..."

    var body: some View {
        VStack(spacing: 16) {
            ProgressView()
                .scaleEffect(1.5)
            Text(message)
                .font(.subheadline)
                .foregroundColor(.secondary)
        }
    }
}

#Preview {
    LoadingView()
}

#Preview("Custom Message") {
    LoadingView(message: "Fetching your results...")
}
