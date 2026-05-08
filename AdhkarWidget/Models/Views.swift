import SwiftUI

struct BackgroundView: View {
    @State private var animate = false

    var body: some View {
        ZStack {
            LinearGradient(
                gradient: Gradient(colors: [
                    Color(red: 0.05, green: 0.15, blue: 0.20),
                    Color(red: 0.08, green: 0.35, blue: 0.30),
                    Color(red: 0.12, green: 0.20, blue: 0.25),
                ]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()

            IslamicPatternBackground()
                .opacity(0.12)

            VStack {
                Circle()
                    .fill(Color(red: 0.25, green: 0.65, blue: 0.50).opacity(0.2))
                    .blur(radius: 80)
                    .frame(width: 250, height: 250)
                    .offset(x: animate ? 100 : -60, y: animate ? -80 : 40)
                Spacer()
                Circle()
                    .fill(Color(red: 0.80, green: 0.60, blue: 0.20).opacity(0.10))
                    .blur(radius: 100)
                    .frame(width: 300, height: 300)
                    .offset(x: animate ? -80 : 60, y: animate ? 60 : -40)
            }
        }
        .onAppear {
            withAnimation(.easeInOut(duration: 6).repeatForever(autoreverses: true)) {
                animate.toggle()
            }
        }
    }
}

struct IslamicPatternBackground: View {
    var body: some View {
        GeometryReader { geo in
            ZStack {
                ForEach(0..<6, id: \.self) { i in
                    IslamicStar()
                        .stroke(Color.white.opacity(0.08), lineWidth: 1)
                        .frame(width: geo.size.width * 0.5, height: geo.size.width * 0.5)
                        .rotationEffect(.degrees(Double(i) * 30))
                }

                ForEach(0..<4, id: \.self) { i in
                    IslamicStar()
                        .stroke(Color(red: 0.70, green: 0.55, blue: 0.20).opacity(0.06), lineWidth: 0.5)
                        .frame(width: geo.size.width * 0.35, height: geo.size.width * 0.35)
                        .rotationEffect(.degrees(Double(i) * 45 + 15))
                }
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
        }
    }
}

struct IslamicStar: Shape {
    func path(in rect: CGRect) -> Path {
        var path = Path()
        let center = CGPoint(x: rect.midX, y: rect.midY)
        let radius = min(rect.width, rect.height) / 2
        let points = 8
        let outerRadius = radius
        let innerRadius = radius * 0.4

        for i in 0..<points {
            let angle = (Double(i) * 360.0 / Double(points) - 90) * .pi / 180
            let isOuter = i % 2 == 0
            let r = isOuter ? outerRadius : innerRadius
            let x = center.x + CGFloat(cos(angle)) * r
            let y = center.y + CGFloat(sin(angle)) * r

            if i == 0 {
                path.move(to: CGPoint(x: x, y: y))
            } else {
                path.addLine(to: CGPoint(x: x, y: y))
            }
        }
        path.closeSubpath()
        return path
    }
}

struct GlassCard<Content: View>: View {
    var content: Content

    init(@ViewBuilder content: () -> Content) {
        self.content = content()
    }

    var body: some View {
        content
            .padding()
            .frame(maxWidth: .infinity)
            .background(
                ZStack {
                    RoundedRectangle(cornerRadius: 24)
                        .fill(.ultraThinMaterial)
                    RoundedRectangle(cornerRadius: 24)
                        .fill(
                            LinearGradient(
                                colors: [.white.opacity(0.12), .white.opacity(0.02)],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            )
                        )
                    RoundedRectangle(cornerRadius: 24)
                        .stroke(
                            LinearGradient(
                                colors: [.white.opacity(0.3), .white.opacity(0.05), .white.opacity(0.1)],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            ),
                            lineWidth: 1
                        )
                }
            )
            .clipShape(RoundedRectangle(cornerRadius: 24))
    }
}

struct AnimatedIcon: View {
    let systemName: String
    @State private var animate = false

    var body: some View {
        Image(systemName: systemName)
            .font(.title3)
            .foregroundColor(.white)
            .frame(width: 44, height: 44)
            .background(
                ZStack {
                    RoundedRectangle(cornerRadius: 14)
                        .fill(.ultraThinMaterial)
                    RoundedRectangle(cornerRadius: 14)
                        .stroke(.white.opacity(0.2), lineWidth: 0.5)
                }
            )
            .scaleEffect(animate ? 1.05 : 1.0)
            .onAppear {
                withAnimation(.spring(response: 1.2, dampingFraction: 0.5).repeatForever(autoreverses: true).delay(Double.random(in: 0...0.5))) {
                    animate = true
                }
            }
    }
}

struct DecorativeDivider: View {
    var body: some View {
        HStack(spacing: 8) {
            RoundedRectangle(cornerRadius: 1)
                .fill(.white.opacity(0.15))
                .frame(height: 1)
            Image(systemName: "diamond.fill")
                .font(.system(size: 6))
                .foregroundColor(Color(red: 0.70, green: 0.55, blue: 0.20))
            RoundedRectangle(cornerRadius: 1)
                .fill(.white.opacity(0.15))
                .frame(height: 1)
        }
    }
}
