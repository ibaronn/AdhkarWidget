import SwiftUI

struct ContentView: View {
    @State private var showContent = false
    @State private var selectedFeature: Int? = nil
    @State private var timePreview = Date()

    let timer = Timer.publish(every: 1, on: .main, in: .common).autoconnect()

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 20) {
                    headerSection
                        .opacity(showContent ? 1 : 0)
                        .offset(y: showContent ? 0 : 20)
                    featuresSection
                        .opacity(showContent ? 1 : 0)
                        .offset(y: showContent ? 0 : 30)
                    previewSection
                        .opacity(showContent ? 1 : 0)
                        .offset(y: showContent ? 0 : 40)
                    instructionsSection
                        .opacity(showContent ? 1 : 0)
                        .offset(y: showContent ? 0 : 50)
                }
                .padding()
            }
            .background(BackgroundView())
            .navigationTitle("أذكاري")
            .navigationBarTitleDisplayMode(.inline)
            .toolbarColorScheme(.dark, for: .navigationBar)
            .toolbarBackground(.hidden, for: .navigationBar)
        }
        .onAppear {
            withAnimation(.spring(response: 0.7, dampingFraction: 0.8).delay(0.15)) {
                showContent = true
            }
        }
        .onReceive(timer) { now in
            timePreview = now
        }
    }

    private var headerSection: some View {
        GlassCard {
            VStack(spacing: 12) {
                ZStack {
                    Circle()
                        .fill(Color(red: 0.70, green: 0.55, blue: 0.20).opacity(0.2))
                        .frame(width: 80, height: 80)
                        .blur(radius: 20)

                    Image(systemName: "moon.stars.fill")
                        .font(.system(size: 40))
                        .foregroundColor(.white)
                }

                Text("أذكاري")
                    .font(.largeTitle.bold())
                    .foregroundColor(.white)

                Text("ويدجت إسلامي • الساعة • الأذكار • القرآن • الأدعية")
                    .font(.subheadline)
                    .multilineTextAlignment(.center)
                    .foregroundColor(.white.opacity(0.6))
            }
        }
    }

    private var featuresSection: some View {
        VStack(spacing: 12) {
            FeatureItem(icon: "clock.fill", title: "الساعة والتاريخ", desc: "الوقت والتاريخ الميلادي والهجري مع أيام الأسبوع", selectedFeature: $selectedFeature, index: 0)
            FeatureItem(icon: "hands.sparkles.fill", title: "الأذكار", desc: "أذكار الصباح والمساء وبعد الصلاة والنوم", selectedFeature: $selectedFeature, index: 1)
            FeatureItem(icon: "book.fill", title: "آيات القرآن", desc: "آيات مختارة من القرآن الكريم مع اسم السورة", selectedFeature: $selectedFeature, index: 2)
            FeatureItem(icon: "hands.praying.fill", title: "الأدعية", desc: "مجموعة من الأدعية المأثورة لكل مناسبة", selectedFeature: $selectedFeature, index: 3)
        }
    }

    private var previewSection: some View {
        GlassCard {
            VStack(spacing: 12) {
                HStack {
                    Text("معاينة الـ Widget")
                        .font(.headline)
                        .foregroundColor(.white)
                    Spacer()
                    Image(systemName: "square.grid.2x2")
                        .font(.caption)
                        .foregroundColor(.white.opacity(0.4))
                }

                DecorativeDivider()

                ZStack {
                    RoundedRectangle(cornerRadius: 20)
                        .fill(
                            LinearGradient(
                                colors: [Color(red: 0.08, green: 0.28, blue: 0.22), Color(red: 0.05, green: 0.18, blue: 0.15)],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            )
                        )

                    RoundedRectangle(cornerRadius: 20)
                        .strokeBorder(
                            LinearGradient(
                                colors: [.white.opacity(0.15), .white.opacity(0.03)],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            ),
                            lineWidth: 1
                        )

                    VStack(spacing: 4) {
                        HStack {
                            Image(systemName: "clock.fill")
                                .font(.caption2)
                                .foregroundColor(Color(red: 0.70, green: 0.55, blue: 0.20))
                            Text(timePreview, style: .time)
                                .font(.system(size: 20, weight: .bold, design: .rounded))
                                .foregroundColor(.white)
                            Spacer()
                            Text("١٤٤٧ هـ")
                                .font(.caption2)
                                .foregroundColor(.white.opacity(0.6))
                        }

                        DecorativeDivider()

                        Spacer(minLength: 2)

                        Text("سُبْحَانَ اللَّهِ وَبِحَمْدِهِ، سُبْحَانَ اللَّهِ الْعَظِيمِ")
                            .font(.system(size: 16, design: .serif))
                            .foregroundColor(.white)
                            .multilineTextAlignment(.center)
                            .lineSpacing(4)

                        Spacer(minLength: 2)

                        HStack {
                            Image(systemName: "hands.sparkles.fill")
                                .font(.caption2)
                                .foregroundColor(Color(red: 0.70, green: 0.55, blue: 0.20))
                            Text("أذكار عامة")
                                .font(.caption2)
                                .foregroundColor(.white.opacity(0.5))
                            Spacer()
                        }
                    }
                    .padding(14)
                }
                .frame(height: 150)
            }
        }
    }

    private var instructionsSection: some View {
        GlassCard {
            VStack(spacing: 10) {
                HStack {
                    Image(systemName: "info.circle.fill")
                        .foregroundColor(Color(red: 0.70, green: 0.55, blue: 0.20))
                    Text("كيفية الإضافة للشاشة الرئيسية")
                        .font(.subheadline)
                        .foregroundColor(.white)
                    Spacer()
                }

                DecorativeDivider()

                VStack(alignment: .trailing, spacing: 8) {
                    instructionStep("1", "اضغط مطولاً على الشاشة الرئيسية")
                    instructionStep("2", "اختر \"أضف Widget\" من الأعلى")
                    instructionStep("3", "ابحث عن \"أذكاري\" واختر الحجم المناسب")
                    instructionStep("4", "اضغط \"إضافة Widget\"")
                }
            }
        }
    }

    private func instructionStep(_ number: String, _ text: String) -> some View {
        HStack(spacing: 10) {
            Text(number)
                .font(.caption.bold())
                .foregroundColor(Color(red: 0.05, green: 0.15, blue: 0.20))
                .frame(width: 22, height: 22)
                .background(Color(red: 0.70, green: 0.55, blue: 0.20))
                .clipShape(Circle())

            Text(text)
                .font(.caption)
                .foregroundColor(.white.opacity(0.65))
            Spacer()
        }
    }
}

struct FeatureItem: View {
    let icon: String
    let title: String
    let desc: String
    @Binding var selectedFeature: Int?
    let index: Int
    @State private var isSelected = false

    var body: some View {
        GlassCard {
            HStack(spacing: 14) {
                AnimatedIcon(systemName: icon)

                VStack(alignment: .trailing, spacing: 4) {
                    Text(title)
                        .font(.headline)
                        .foregroundColor(.white)

                    Text(desc)
                        .font(.caption)
                        .foregroundColor(.white.opacity(0.55))
                        .lineLimit(isSelected ? nil : 1)
                }

                Spacer(minLength: 0)
            }
        }
        .scaleEffect(isSelected ? 1.02 : 1)
        .onTapGesture {
            withAnimation(.spring(response: 0.3, dampingFraction: 0.6)) {
                isSelected.toggle()
                selectedFeature = isSelected ? index : nil
            }
        }
    }
}

#Preview {
    ContentView()
}
