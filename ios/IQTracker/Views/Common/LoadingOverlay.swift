import SwiftUI

/// A full-screen loading overlay with spinner and optional message
struct LoadingOverlay: View {
    let message: String?

    init(message: String? = nil) {
        self.message = message
    }

    var body: some View {
        ZStack {
            Color.black.opacity(0.4)
                .ignoresSafeArea()

            VStack(spacing: 16) {
                ProgressView()
                    .progressViewStyle(CircularProgressViewStyle(tint: .white))
                    .scaleEffect(1.5)

                if let message {
                    Text(message)
                        .font(.subheadline)
                        .foregroundColor(.white)
                }
            }
            .padding(32)
            .background(Color(.systemGray6))
            .cornerRadius(16)
            .shadow(radius: 10)
        }
    }
}

#Preview {
    ZStack {
        Color.blue
            .ignoresSafeArea()

        LoadingOverlay(message: "Logging in...")
    }
}
