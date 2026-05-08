import Foundation

struct Zikr: Identifiable, Codable {
    let id = UUID()
    let text: String
    let count: Int
    let source: String
    let category: AdhkarCategory

    enum AdhkarCategory: String, Codable, CaseIterable {
        case morning = "أذكار الصباح"
        case evening = "أذكار المساء"
        case afterPrayer = "أذكار بعد الصلاة"
        case sleep = "أذكار النوم"
        case general = "أذكار عامة"
    }
}

struct Dua: Identifiable, Codable {
    let id = UUID()
    let text: String
    let occasion: String
}

struct QuranVerse: Identifiable, Codable {
    let id = UUID()
    let surah: String
    let ayahNumber: Int
    let text: String
    let translation: String
}
