# دليل إعداد أذكاري - Build سحابي عبر GitHub Actions

## المقدمة
بما أنك لا تملك Mac، هذا الدليل يشرح كيفية بناء تطبيق iOS عبر سحابة GitHub مجاناً.

## المتطلبات
1. **حساب GitHub** - مجاني (https://github.com/signup)
2. **Git** على جهازك - قم بتحميله من (https://git-scm.com/downloads/win)
3. **حساب Apple مجاني** - لتثبيت التطبيق على جهاز iPhone الخاص بك (https://appleid.apple.com)

---

## الخطوة 1: تحميل Git وتثبيته
```bash
# حمل Git من: https://git-scm.com/downloads/win
# ثم تأكد من التثبيت:
git --version
```

## الخطوة 2: إنشاء مستودع على GitHub
1. اذهب إلى https://github.com/new
2. اسم المستودع: `AdhkarWidget`
3. اختار **Public** أو **Private**
4. لا تختار أي خيارات إضافية (لا README، لا .gitignore)
5. اضغط "Create repository"

## الخطوة 3: رفع الكود إلى GitHub
افتح **PowerShell** أو **CMD** في مجلد `AdhkarWidget` وشغل:

```bash
git init
git add .
git commit -m "Initial commit - AdhkarWidget iOS app"
git branch -M main
git remote add origin https://github.com/<اسم-مستخدمك>/AdhkarWidget.git
git push -u origin main
```

> استبدل `<اسم-مستخدمك>` باسم مستخدم GitHub الخاص بك.

## الخطوة 4: تشغيل GitHub Actions
1. اذهب إلى مستودعك على GitHub
2. اضغط على **Actions** tab
3. ستشاهد workflow اسمه "Build iOS App"
4. اضغط على "Run workflow" → "Run workflow"
5. انتظر حتى ينتهي البناء (5-10 دقائق)

## الخطوة 5: تحميل التطبيق (للـ Simulator)
1. بعد انتهاء البناء، اضغط على الـ workflow
2. ستجد Artifact اسمه `AdhkarWidget-Simulator-Build`
3. حمّله واستخدمه في Xcode على Mac (إذا توفر لاحقاً)

---

## بناء IPA حقيقي (لتثبيته على iPhone)
لبناء IPA حقيقي (لتثبيته على جهازك فعلياً)، تحتاج إلى:

1. **حساب Apple Developer** - مجاني أو مدفوع
2. **إضافة Secrets إلى GitHub**:
   - اذهب إلى Settings → Secrets and variables → Actions
   - أضف:
     - `APPLE_ID`: بريد Apple الخاص بك
     - `APPLE_APP_SPECIFIC_PASSWORD`: كلمة مرور خاصة من Apple (أنشئها من appleid.apple.com)
     - `TEAM_ID`: Team ID من حساب Apple Developer

3. **تعديل ملف `.github/workflows/build.yml`**:
   - غير السطر `if: false` إلى `if: true` في job `build-ipa`
   - ارفع التعديل إلى GitHub

4. **شغل الـ workflow من جديد** - سينتج ملف `.ipa` يمكنك تثبيته على iPhone عبر:
   - AltStore
   - SideStore
   - Xcode (عبر Mac)

---

## هيكل المشروع
```
AdhkarWidget/
├── .github/workflows/build.yml   # CI/CD pipeline
├── AdhkarWidget/                  # ملفات المصدر
│   ├── AdhkarWidgetApp.swift      # مدخل التطبيق
│   ├── ContentView.swift          # الواجهة الرئيسية
│   ├── Info.plist                 # إعدادات التطبيق
│   ├── Models/
│   │   ├── Adhkar.swift           # نماذج البيانات
│   │   └── DataStore.swift        # الأذكار والآيات والأدعية
│   └── Widget/
│       ├── AdhkarWidget.swift     # الـ Widget نفسه
│       └── AdhkarWidgetBundle.swift
├── AdhkarWidgetExtension/
│   └── Info.plist                 # إعدادات الـ Extension
├── project.yml                    # إعدادات XcodeGen
└── SETUP.md                       # هذا الملف
```
