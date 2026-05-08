import SwiftUI

@main
struct AdhkarWidgetApp: App {
    @State private var isSplash = true

    var body: some Scene {
        WindowGroup {
            if isSplash {
                SplashView()
                    .onAppear {
                        withAnimation(.easeInOut(duration: 1.2).delay(0.3)) {
                            isSplash = false
                        }
                    }
            } else {
                ContentView()
                    .transition(.opacity.combined(with: .scale(scale: 0.95)))
            }
        }
    }
}

struct SplashView: View {
    @State private var scale: CGFloat = 0.5
    @State private var opacity: Double = 0
    @State private var rotation: Double = -30

    var body: some View {
        ZStack {
            BackgroundView()
            VStack(spacing: 16) {
                Image(systemName: "moon.stars.fill")
                    .font(.system(size: 60))
                    .foregroundColor(.white)
                    .rotationEffect(.degrees(rotation))
                    .scaleEffect(scale)

                Text("أذكاري")
                    .font(.largeTitle.bold())
                    .foregroundColor(.white)
                    .opacity(opacity)

                Text("الساعة • الأذكار • القرآن • الأدعية")
                    .font(.subheadline)
                    .foregroundColor(.white.opacity(0.7))
                    .opacity(opacity)
            }
        }
        .onAppear {
            withAnimation(.spring(response: 0.8, dampingFraction: 0.6).delay(0.1)) {
                scale = 1.0
                rotation = 0
            }
            withAnimation(.easeOut(duration: 0.6).delay(0.4)) {
                opacity = 1
            }
        }
    }
}
