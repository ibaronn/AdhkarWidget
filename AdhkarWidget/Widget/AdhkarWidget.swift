import WidgetKit
import SwiftUI

struct AdhkarEntry: TimelineEntry {
    let date: Date
    let hijriDate: String
    let weekday: String
    let contentType: WidgetContentType
    let contentText: String
    let contentSubtext: String
}

struct AdhkarProvider: TimelineProvider {
    func placeholder(in context: Context) -> AdhkarEntry {
        AdhkarEntry(
            date: Date(),
            hijriDate: "١٤٤٧ هـ",
            weekday: "الجمعة",
            contentType: .zikr,
            contentText: "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ",
            contentSubtext: "أذكار الصباح"
        )
    }

    func getSnapshot(in context: Context, completion: @escaping (AdhkarEntry) -> Void) {
        completion(makeEntry(for: Date()))
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<AdhkarEntry>) -> Void) {
        let entry = makeEntry(for: Date())
        let nextUpdate = Calendar.current.date(byAdding: .hour, value: 1, to: Date()) ?? Date()
        let timeline = Timeline(entries: [entry], policy: .after(nextUpdate))
        completion(timeline)
    }

    private func makeEntry(for date: Date) -> AdhkarEntry {
        let cal = Calendar(identifier: .gregorian)
        let day = cal.component(.day, from: date)
        let month = cal.component(.month, from: date)
        let year = cal.component(.year, from: date)
        let weekdayIndex = cal.component(.weekday, from: date)

        let weekdays = ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"]
        let weekdayName = weekdays[weekdayIndex - 1]

        let hijri = Calendar(identifier: .islamicUmmAlQura)
        let hDay = hijri.component(.day, from: date)
        let hMonth = hijri.component(.month, from: date)
        let hYear = hijri.component(.year, from: date)
        let hijriMonths = ["محرم", "صفر", "ربيع الأول", "ربيع الآخر", "جمادى الأولى", "جمادى الآخرة", "رجب", "شعبان", "رمضان", "شوال", "ذو القعدة", "ذو الحجة"]
        let hijriMonthName = hijriMonths[hMonth - 1]
        let hijriStr = "\(hDay) \(hijriMonthName) \(hYear) هـ"

        let roll = Int.random(in: 0..<3)
        let type: WidgetContentType
        var text: String
        var subtext: String

        switch roll {
        case 0:
            type = .zikr
            let z = DataStore.randomZikr()
            text = z.text
            subtext = z.category.rawValue
        case 1:
            type = .dua
            let d = DataStore.randomDua()
            text = d.text
            subtext = d.occasion
        default:
            type = .quran
            let q = DataStore.randomQuranVerse()
            text = q.text
            subtext = "سورة \(q.surah) - آية \(q.ayahNumber)"
        }

        return AdhkarEntry(
            date: date,
            hijriDate: hijriStr,
            weekday: weekdayName,
            contentType: type,
            contentText: text,
            contentSubtext: subtext
        )
    }
}

struct AdhkarWidgetEntryView: View {
    var entry: AdhkarEntry

    var body: some View {
        VStack(spacing: 0) {
            headerView
            decorativeBar
            contentView
        }
        .padding(12)
        .background(
            ZStack {
                LinearGradient(
                    colors: [
                        Color(red: 0.06, green: 0.20, blue: 0.16),
                        Color(red: 0.09, green: 0.30, blue: 0.24),
                        Color(red: 0.05, green: 0.15, blue: 0.12),
                    ],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )

                RoundedRectangle(cornerRadius: 24)
                    .fill(.white.opacity(0.04))

                RoundedRectangle(cornerRadius: 24)
                    .strokeBorder(
                        LinearGradient(
                            colors: [.white.opacity(0.12), .white.opacity(0.03)],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        ),
                        lineWidth: 1
                    )

                VStack {
                    HStack {
                        IslamicStar()
                            .stroke(.white.opacity(0.04), lineWidth: 1)
                            .frame(width: 60, height: 60)
                        Spacer()
                        IslamicStar()
                            .stroke(.white.opacity(0.03), lineWidth: 0.5)
                            .frame(width: 40, height: 40)
                    }
                    Spacer()
                    HStack {
                        IslamicStar()
                            .stroke(.white.opacity(0.025), lineWidth: 0.5)
                            .frame(width: 35, height: 35)
                        Spacer()
                        IslamicStar()
                            .stroke(.white.opacity(0.035), lineWidth: 0.8)
                            .frame(width: 50, height: 50)
                    }
                }
                .padding(8)
            }
        )
    }

    private var headerView: some View {
        VStack(spacing: 4) {
            HStack(alignment: .firstTextBaseline) {
                Image(systemName: "clock.fill")
                    .font(.caption2)
                    .foregroundColor(Color(red: 0.75, green: 0.60, blue: 0.25))
                Text(entry.date, style: .time)
                    .font(.system(size: 20, weight: .bold, design: .rounded))
                    .foregroundColor(.white)
                Spacer()
                Text(entry.hijriDate)
                    .font(.caption2)
                    .foregroundColor(.white.opacity(0.5))
            }

            HStack {
                Text(entry.weekday)
                    .font(.caption)
                    .foregroundColor(.white.opacity(0.6))
                Spacer()
            }
        }
    }

    private var decorativeBar: some View {
        HStack(spacing: 6) {
            RoundedRectangle(cornerRadius: 0.5)
                .fill(.white.opacity(0.08))
                .frame(height: 0.5)
            Image(systemName: "diamond.fill")
                .font(.system(size: 4))
                .foregroundColor(Color(red: 0.70, green: 0.55, blue: 0.20))
            RoundedRectangle(cornerRadius: 0.5)
                .fill(.white.opacity(0.08))
                .frame(height: 0.5)
        }
        .padding(.vertical, 6)
    }

    private var contentView: some View {
        VStack(spacing: 4) {
            Spacer(minLength: 2)

            ScrollView {
                Text(entry.contentText)
                    .font(.system(size: 17, design: .serif))
                    .fontWeight(.medium)
                    .multilineTextAlignment(.center)
                    .foregroundColor(.white)
                    .lineSpacing(3)
            }

            Spacer(minLength: 2)

            HStack(spacing: 6) {
                Circle()
                    .fill(typeColor)
                    .frame(width: 6, height: 6)
                Text(entry.contentSubtext)
                    .font(.caption2)
                    .foregroundColor(.white.opacity(0.45))
                Spacer()
            }
        }
    }

    private var typeColor: Color {
        switch entry.contentType {
        case .zikr: return Color(red: 0.50, green: 0.80, blue: 0.50)
        case .dua: return Color(red: 0.75, green: 0.60, blue: 0.25)
        case .quran: return Color(red: 0.40, green: 0.70, blue: 0.90)
        }
    }
}

struct AdhkarWidget: Widget {
    let kind: String = "AdhkarWidget"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: AdhkarProvider()) { entry in
            AdhkarWidgetEntryView(entry: entry)
                .containerBackground(.clear, for: .widget)
        }
        .configurationDisplayName("أذكاري")
        .description("الساعة • الأذكار • القرآن • الأدعية")
        .supportedFamilies([.systemMedium, .systemLarge])
    }
}
