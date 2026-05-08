#!/usr/bin/env python3

import os
import uuid

def uid():
    return uuid.uuid4().hex[:24].upper()

def write_pbxproj():
    # Generate UUIDs
    root_id = uid()
    project_id = uid()
    main_group_id = uid()
    app_group_id = uid()
    models_group_id = uid()
    widget_group_id = uid()
    ext_group_id = uid()
    products_group_id = uid()

    app_target_id = uid()
    ext_target_id = uid()

    app_sources_id = uid()
    app_resources_id = uid()
    ext_sources_id = uid()
    ext_resources_id = uid()
    embed_phase_id = uid()

    app_debug_id = uid()
    app_release_id = uid()
    app_config_list_id = uid()
    ext_debug_id = uid()
    ext_release_id = uid()
    ext_config_list_id = uid()
    proj_debug_id = uid()
    proj_release_id = uid()
    proj_config_list_id = uid()

    app_product_id = uid()
    ext_product_id = uid()

    dep_id = uid()
    embed_file_id = uid()

    # File references
    fref = {}
    src_files = ["AdhkarWidget/AdhkarWidgetApp.swift", "AdhkarWidget/ContentView.swift",
                 "AdhkarWidget/Models/Adhkar.swift", "AdhkarWidget/Models/DataStore.swift",
                 "AdhkarWidget/Models/Views.swift"]
    ext_files = ["AdhkarWidget/Widget/AdhkarWidget.swift", "AdhkarWidget/Widget/AdhkarWidgetBundle.swift",
                 "AdhkarWidget/Models/Adhkar.swift", "AdhkarWidget/Models/DataStore.swift",
                 "AdhkarWidget/Models/Views.swift"]
    all_files = list(set(src_files + ext_files + ["AdhkarWidget/Info.plist", "AdhkarWidgetExtension/Info.plist"]))

    for f in all_files:
        fref[f] = uid()

    # Build files
    bref = {}
    for f in all_files:
        bref[f] = uid()

    lines = []
    lines.append('// !$*UTF8*$!')
    lines.append('{')
    lines.append('\tarchiveVersion = 1;')
    lines.append('\tclasses = {};')
    lines.append('\tobjectVersion = 56;')
    lines.append('\tobjects = {')

    # PBXBuildFile
    lines.append('\n/* Begin PBXBuildFile section */')
    for f, bid in bref.items():
        fid = fref[f]
        settings = ''
        if f == 'AdhkarWidgetExtension/Info.plist':
            settings = '; settings = {ATTRIBUTES = (Primary, ); }'
        lines.append(f'\t\t{bid} /* {f} in Sources */ = {{isa = PBXBuildFile; fileRef = {fid} /* {f} */{settings}; }};')
    lines.append(f'\t\t{embed_file_id} /* AdhkarWidgetExtension.appex in Embed App Extensions */ = {{isa = PBXBuildFile; fileRef = {ext_product_id} /* AdhkarWidgetExtension.appex */; settings = {{ATTRIBUTES = (RemoveHeadersOnCopy, ); }}; }};')
    lines.append('/* End PBXBuildFile section */')

    # PBXFileReference
    lines.append('\n/* Begin PBXFileReference section */')
    for f, fid in fref.items():
        name = os.path.basename(f)
        ext = os.path.splitext(f)[1]
        if ext == '.swift':
            ftype = 'sourcecode.swift'
        elif ext == '.plist':
            ftype = 'text.plist.xml'
        else:
            ftype = 'file'
        lines.append(f'\t\t{fid} /* {name} */ = {{isa = PBXFileReference; fileEncoding = 4; lastKnownFileType = {ftype}; name = {name}; path = {f}; sourceTree = SOURCE_ROOT; }};')
    lines.append(f'\t\t{app_product_id} /* AdhkarWidget.app */ = {{isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = AdhkarWidget.app; sourceTree = BUILT_PRODUCTS_DIR; }};')
    lines.append(f'\t\t{ext_product_id} /* AdhkarWidgetExtension.appex */ = {{isa = PBXFileReference; explicitFileType = "wrapper.app-extension"; includeInIndex = 0; path = AdhkarWidgetExtension.appex; sourceTree = BUILT_PRODUCTS_DIR; }};')
    lines.append('/* End PBXFileReference section */')

    # PBXFrameworksBuildPhase
    fw_id = uid()
    lines.append('\n/* Begin PBXFrameworksBuildPhase section */')
    lines.append(f'\t\t{fw_id} /* Frameworks */ = {{isa = PBXFrameworksBuildPhase; buildActionMask = 2147483647; files = (); runOnlyForDeploymentPostprocessing = 0; }};')
    lines.append('/* End PBXFrameworksBuildPhase section */')

    # PBXGroup
    lines.append('\n/* Begin PBXGroup section */')
    lines.append(f'\t\t{products_group_id} /* Products */ = {{')
    lines.append('\t\t\tisa = PBXGroup;')
    lines.append('\t\t\tchildren = (')
    lines.append(f'\t\t\t\t{app_product_id} /* AdhkarWidget.app */,')
    lines.append(f'\t\t\t\t{ext_product_id} /* AdhkarWidgetExtension.appex */,')
    lines.append('\t\t\t);')
    lines.append('\t\t\tname = Products;')
    lines.append('\t\t\tsourceTree = "<group>";')
    lines.append('\t\t};')

    # Main group
    lines.append(f'\t\t{app_group_id} /* AdhkarWidget */ = {{')
    lines.append('\t\t\tisa = PBXGroup;')
    lines.append('\t\t\tchildren = (')
    lines.append(f'\t\t\t\t{fref["AdhkarWidget/AdhkarWidgetApp.swift"]} /* AdhkarWidgetApp.swift */,')
    lines.append(f'\t\t\t\t{fref["AdhkarWidget/ContentView.swift"]} /* ContentView.swift */,')
    lines.append(f'\t\t\t\t{models_group_id} /* Models */,')
    lines.append(f'\t\t\t\t{widget_group_id} /* Widget */,')
    lines.append(f'\t\t\t\t{fref["AdhkarWidget/Info.plist"]} /* Info.plist */,')
    lines.append('\t\t\t);')
    lines.append('\t\t\tname = AdhkarWidget;')
    lines.append('\t\t\tpath = AdhkarWidget;')
    lines.append('\t\t\tsourceTree = SOURCE_ROOT;')
    lines.append('\t\t};')

    lines.append(f'\t\t{models_group_id} /* Models */ = {{')
    lines.append('\t\t\tisa = PBXGroup;')
    lines.append('\t\t\tchildren = (')
    lines.append(f'\t\t\t\t{fref["AdhkarWidget/Models/Adhkar.swift"]} /* Adhkar.swift */,')
    lines.append(f'\t\t\t\t{fref["AdhkarWidget/Models/DataStore.swift"]} /* DataStore.swift */,')
    lines.append(f'\t\t\t\t{fref["AdhkarWidget/Models/Views.swift"]} /* Views.swift */,')
    lines.append('\t\t\t);')
    lines.append('\t\t\tname = Models;')
    lines.append('\t\t\tpath = Models;')
    lines.append('\t\t\tsourceTree = SOURCE_ROOT;')
    lines.append('\t\t};')

    lines.append(f'\t\t{widget_group_id} /* Widget */ = {{')
    lines.append('\t\t\tisa = PBXGroup;')
    lines.append('\t\t\tchildren = (')
    lines.append(f'\t\t\t\t{fref["AdhkarWidget/Widget/AdhkarWidget.swift"]} /* AdhkarWidget.swift */,')
    lines.append(f'\t\t\t\t{fref["AdhkarWidget/Widget/AdhkarWidgetBundle.swift"]} /* AdhkarWidgetBundle.swift */,')
    lines.append('\t\t\t);')
    lines.append('\t\t\tname = Widget;')
    lines.append('\t\t\tpath = Widget;')
    lines.append('\t\t\tsourceTree = SOURCE_ROOT;')
    lines.append('\t\t};')

    lines.append(f'\t\t{ext_group_id} /* AdhkarWidgetExtension */ = {{')
    lines.append('\t\t\tisa = PBXGroup;')
    lines.append('\t\t\tchildren = (')
    lines.append(f'\t\t\t\t{fref["AdhkarWidgetExtension/Info.plist"]} /* Info.plist */,')
    lines.append('\t\t\t);')
    lines.append('\t\t\tname = AdhkarWidgetExtension;')
    lines.append('\t\t\tpath = AdhkarWidgetExtension;')
    lines.append('\t\t\tsourceTree = SOURCE_ROOT;')
    lines.append('\t\t};')

    lines.append(f'\t\t{main_group_id} = {{')
    lines.append('\t\t\tisa = PBXGroup;')
    lines.append('\t\t\tchildren = (')
    lines.append(f'\t\t\t\t{app_group_id} /* AdhkarWidget */,')
    lines.append(f'\t\t\t\t{ext_group_id} /* AdhkarWidgetExtension */,')
    lines.append(f'\t\t\t\t{products_group_id} /* Products */,')
    lines.append('\t\t\t);')
    lines.append('\t\t\tsourceTree = "<group>";')
    lines.append('\t\t};')
    lines.append('/* End PBXGroup section */')

    # PBXNativeTarget
    lines.append('\n/* Begin PBXNativeTarget section */')
    lines.append(f'\t\t{app_target_id} /* AdhkarWidget */ = {{')
    lines.append('\t\t\tisa = PBXNativeTarget;')
    lines.append(f'\t\t\tbuildConfigurationList = {app_config_list_id};')
    lines.append('\t\t\tbuildPhases = (')
    lines.append(f'\t\t\t\t{app_sources_id} /* Sources */,')
    lines.append(f'\t\t\t\t{fw_id} /* Frameworks */,')
    lines.append(f'\t\t\t\t{app_resources_id} /* Resources */,')
    lines.append(f'\t\t\t\t{embed_phase_id} /* Embed App Extensions */,')
    lines.append('\t\t\t);')
    lines.append('\t\t\tbuildRules = ();')
    lines.append('\t\t\tdependencies = (')
    lines.append(f'\t\t\t\t{dep_id} /* PBXTargetDependency */,')
    lines.append('\t\t\t);')
    lines.append('\t\t\tname = AdhkarWidget;')
    lines.append('\t\t\tproductName = AdhkarWidget;')
    lines.append(f'\t\t\tproductReference = {app_product_id};')
    lines.append('\t\t\tproductType = "com.apple.product-type.application";')
    lines.append('\t\t};')

    lines.append(f'\t\t{ext_target_id} /* AdhkarWidgetExtension */ = {{')
    lines.append('\t\t\tisa = PBXNativeTarget;')
    lines.append(f'\t\t\tbuildConfigurationList = {ext_config_list_id};')
    lines.append('\t\t\tbuildPhases = (')
    lines.append(f'\t\t\t\t{ext_sources_id} /* Sources */,')
    lines.append(f'\t\t\t\t{uid()} /* Frameworks */,')
    lines.append(f'\t\t\t\t{ext_resources_id} /* Resources */,')
    lines.append('\t\t\t);')
    lines.append('\t\t\tbuildRules = ();')
    lines.append('\t\t\tdependencies = ();')
    lines.append('\t\t\tname = AdhkarWidgetExtension;')
    lines.append('\t\t\tproductName = AdhkarWidgetExtension;')
    lines.append(f'\t\t\tproductReference = {ext_product_id};')
    lines.append('\t\t\tproductType = "com.apple.product-type.app-extension";')
    lines.append('\t\t};')
    lines.append('/* End PBXNativeTarget section */')

    # PBXProject
    lines.append('\n/* Begin PBXProject section */')
    lines.append(f'\t\t{project_id} /* Project object */ = {{')
    lines.append('\t\t\tisa = PBXProject;')
    lines.append(f'\t\t\tbuildConfigurationList = {proj_config_list_id};')
    lines.append('\t\t\tcompatibilityVersion = "Xcode 14.0";')
    lines.append('\t\t\tdevelopmentRegion = "ar";')
    lines.append('\t\t\thasScannedForEncodings = 0;')
    lines.append('\t\t\tknownRegions = ("en", "ar", "Base");')
    lines.append(f'\t\t\tmainGroup = {main_group_id};')
    lines.append(f'\t\t\tproductRefGroup = {products_group_id};')
    lines.append('\t\t\tprojectDirPath = "";')
    lines.append('\t\t\tprojectRoot = "";')
    lines.append('\t\t\ttargets = (')
    lines.append(f'\t\t\t\t{app_target_id} /* AdhkarWidget */,')
    lines.append(f'\t\t\t\t{ext_target_id} /* AdhkarWidgetExtension */,')
    lines.append('\t\t\t);')
    lines.append('\t\t};')
    lines.append('/* End PBXProject section */')

    # PBXResourcesBuildPhase
    lines.append('\n/* Begin PBXResourcesBuildPhase section */')
    lines.append(f'\t\t{app_resources_id} /* Resources */ = {{')
    lines.append('\t\t\tisa = PBXResourcesBuildPhase; buildActionMask = 2147483647; files = (); runOnlyForDeploymentPostprocessing = 0;')
    lines.append('\t\t};')
    lines.append(f'\t\t{ext_resources_id} /* Resources */ = {{')
    lines.append('\t\t\tisa = PBXResourcesBuildPhase; buildActionMask = 2147483647; files = (); runOnlyForDeploymentPostprocessing = 0;')
    lines.append('\t\t};')
    lines.append('/* End PBXResourcesBuildPhase section */')

    # PBXCopyFilesBuildPhase (Embed)
    lines.append('\n/* Begin PBXCopyFilesBuildPhase section */')
    lines.append(f'\t\t{embed_phase_id} /* Embed App Extensions */ = {{')
    lines.append('\t\t\tisa = PBXCopyFilesBuildPhase;')
    lines.append('\t\t\tbuildActionMask = 2147483647;')
    lines.append('\t\t\tdstPath = "";')
    lines.append('\t\t\tdstSubfolderSpec = 13;')
    lines.append('\t\t\tfiles = (')
    lines.append(f'\t\t\t\t{embed_file_id} /* AdhkarWidgetExtension.appex in Embed App Extensions */,')
    lines.append('\t\t\t);')
    lines.append('\t\t\tname = "Embed App Extensions";')
    lines.append('\t\t\trunOnlyForDeploymentPostprocessing = 0;')
    lines.append('\t\t};')
    lines.append('/* End PBXCopyFilesBuildPhase section */')

    # PBXSourcesBuildPhase
    lines.append('\n/* Begin PBXSourcesBuildPhase section */')
    lines.append(f'\t\t{app_sources_id} /* Sources */ = {{')
    lines.append('\t\t\tisa = PBXSourcesBuildPhase;')
    lines.append('\t\t\tbuildActionMask = 2147483647;')
    lines.append('\t\t\tfiles = (')
    for f in src_files:
        lines.append(f'\t\t\t\t{bref[f]} /* {os.path.basename(f)} in Sources */,')
    lines.append('\t\t\t);')
    lines.append('\t\t\trunOnlyForDeploymentPostprocessing = 0;')
    lines.append('\t\t};')

    lines.append(f'\t\t{ext_sources_id} /* Sources */ = {{')
    lines.append('\t\t\tisa = PBXSourcesBuildPhase;')
    lines.append('\t\t\tbuildActionMask = 2147483647;')
    lines.append('\t\t\tfiles = (')
    for f in ext_files:
        lines.append(f'\t\t\t\t{bref[f]} /* {os.path.basename(f)} in Sources */,')
    lines.append('\t\t\t);')
    lines.append('\t\t\trunOnlyForDeploymentPostprocessing = 0;')
    lines.append('\t\t};')
    lines.append('/* End PBXSourcesBuildPhase section */')

    # PBXTargetDependency
    lines.append('\n/* Begin PBXTargetDependency section */')
    lines.append(f'\t\t{dep_id} /* PBXTargetDependency */ = {{')
    lines.append('\t\t\tisa = PBXTargetDependency;')
    lines.append(f'\t\t\ttarget = {ext_target_id} /* AdhkarWidgetExtension */;')
    lines.append(f'\t\t\ttargetProxy = {uid()} /* PBXContainerItemProxy */;')
    lines.append('\t\t};')
    lines.append('/* End PBXTargetDependency section */')

    # XCBuildConfiguration
    lines.append('\n/* Begin XCBuildConfiguration section */')

    def write_build_config(name, settings):
        cid = uid()
        lines.append(f'\t\t{cid} /* {name} */ = {{')
        lines.append('\t\t\tisa = XCBuildConfiguration;')
        lines.append('\t\t\tbuildSettings = {')
        for k, v in settings.items():
            lines.append(f'\t\t\t\t{k} = {v};')
        lines.append('\t\t\t};')
        lines.append(f'\t\t\tname = {name};')
        lines.append('\t\t};')
        return cid

    # App configs
    app_common = {
        'ASSETCATALOG_COMPILER_APPICON_NAME': 'AppIcon',
        'CODE_SIGN_IDENTITY': '"-"',
        'CODE_SIGN_STYLE': 'Manual',
        'CURRENT_PROJECT_VERSION': '1',
        'INFOPLIST_FILE': '"AdhkarWidget/Info.plist"',
        'IPHONEOS_DEPLOYMENT_TARGET': '"17.0"',
        'MARKETING_VERSION': '"1.0"',
        'PRODUCT_BUNDLE_IDENTIFIER': '"com.adhkar.widgetapp"',
        'PRODUCT_NAME': '"$(TARGET_NAME)"',
        'SWIFT_VERSION': '"5.0"',
        'TARGETED_DEVICE_FAMILY': '"1,2"',
        'GENERATE_INFOPLIST_FILE': 'NO',
    }
    app_debug_s = dict(app_common, **{'SWIFT_OPTIMIZATION_LEVEL': '"-Onone"'})
    app_release_s = dict(app_common)
    write_build_config('Debug', app_debug_s)
    write_build_config('Release', app_release_s)

    # Extension configs
    ext_common = {
        'CODE_SIGN_IDENTITY': '"-"',
        'CODE_SIGN_STYLE': 'Manual',
        'CURRENT_PROJECT_VERSION': '1',
        'INFOPLIST_FILE': '"AdhkarWidgetExtension/Info.plist"',
        'IPHONEOS_DEPLOYMENT_TARGET': '"17.0"',
        'MARKETING_VERSION': '"1.0"',
        'PRODUCT_BUNDLE_IDENTIFIER': '"com.adhkar.widgetapp.extension"',
        'PRODUCT_NAME': '"$(TARGET_NAME)"',
        'SKIP_INSTALL': 'YES',
        'SWIFT_VERSION': '"5.0"',
        'GENERATE_INFOPLIST_FILE': 'NO',
    }
    ext_debug_s = dict(ext_common, **{'SWIFT_OPTIMIZATION_LEVEL': '"-Onone"'})
    ext_release_s = dict(ext_common)
    write_build_config('Debug', ext_debug_s)
    write_build_config('Release', ext_release_s)

    # Project-level configs
    proj_common = {
        'ALWAYS_SEARCH_USER_PATHS': 'NO',
        'CLANG_ANALYZER_NONNULL': 'YES',
        'CLANG_CXX_LANGUAGE_STANDARD': '"gnu++14"',
        'CLANG_ENABLE_MODULES': 'YES',
        'CLANG_ENABLE_OBJC_ARC': 'YES',
        'COPY_PHASE_STRIP': 'NO',
        'ENABLE_STRICT_OBJC_MSGSEND': 'YES',
        'GCC_OPTIMIZATION_LEVEL': '0',
        'GCC_PREPROCESSOR_DEFINITIONS': '("DEBUG=1", "$(inherited)")',
        'IPHONEOS_DEPLOYMENT_TARGET': '"17.0"',
        'MTL_ENABLE_DEBUG_INFO': 'INCLUDE_SOURCE',
        'ONLY_ACTIVE_ARCH': 'YES',
        'SDKROOT': 'iphoneos',
        'SWIFT_ACTIVE_COMPILATION_CONDITIONS': '"DEBUG"',
        'SWIFT_OPTIMIZATION_LEVEL': '"-Onone"',
    }
    proj_release = {
        'ALWAYS_SEARCH_USER_PATHS': 'NO',
        'CLANG_ANALYZER_NONNULL': 'YES',
        'CLANG_CXX_LANGUAGE_STANDARD': '"gnu++14"',
        'CLANG_ENABLE_MODULES': 'YES',
        'CLANG_ENABLE_OBJC_ARC': 'YES',
        'COPY_PHASE_STRIP': 'NO',
        'ENABLE_NS_ASSERTIONS': 'NO',
        'ENABLE_STRICT_OBJC_MSGSEND': 'YES',
        'GCC_OPTIMIZATION_LEVEL': 's',
        'IPHONEOS_DEPLOYMENT_TARGET': '"17.0"',
        'MTL_ENABLE_DEBUG_INFO': 'NO',
        'SDKROOT': 'iphoneos',
        'SWIFT_COMPILATION_MODE': 'wholemodule',
        'SWIFT_OPTIMIZATION_LEVEL': '"-O"',
        'VALIDATE_PRODUCT': 'YES',
    }
    proj_debug_id = write_build_config('Debug', proj_common)
    proj_release_id = write_build_config('Release', proj_release)
    lines.append('/* End XCBuildConfiguration section */')

    # XCConfigurationList
    lines.append('\n/* Begin XCConfigurationList section */')
    lines.append(f'\t\t{proj_config_list_id} = {{')
    lines.append('\t\t\tisa = XCConfigurationList;')
    lines.append('\t\t\tbuildConfigurations = (')
    lines.append(f'\t\t\t\t{proj_debug_id} /* Debug */,')
    lines.append(f'\t\t\t\t{proj_release_id} /* Release */,')
    lines.append('\t\t\t);')
    lines.append('\t\t\tdefaultConfigurationIsVisible = 0;')
    lines.append('\t\t\tdefaultConfigurationName = Release;')
    lines.append('\t\t};')

    # We need to make the app and ext config lists reference the right config IDs
    # But we lost them since write_build_config generated random UUIDs
    # Let me fix this by re-generating and storing them

    # Actually, let me just rewrite this more carefully
    lines = lines[:0]  # Clear

    # Let me just use a simpler approach with proper UUID tracking
    lines = []
    lines.append('// !$*UTF8*$!')
    lines.append('{')
    lines.append('\tarchiveVersion = 1;')
    lines.append('\tclasses = {};')
    lines.append('\tobjectVersion = 56;')
    lines.append('\tobjects = {')

    # Now track all UUIDs we generate
    uuids = {}

    # Generate the config lists properly
    app_debug_id = uid()
    app_release_id = uid()
    app_conf_list_id = uid()
    ext_debug_id = uid()
    ext_release_id = uid()
    ext_conf_list_id = uid()
    proj_debug_cid = uid()
    proj_release_cid = uid()
    proj_conf_list_id = uid()

    # PBXBuildFile
    lines.append('\n/* Begin PBXBuildFile section */')
    for f in all_files:
        bid = uid()
        bref[f] = bid
        fid = fref[f]
        settings = ''
        if f == 'AdhkarWidgetExtension/Info.plist':
            settings = '; settings = {ATTRIBUTES = (Primary, ); }'
        lines.append(f'\t\t{bid} /* {f} in Sources */ = {{isa = PBXBuildFile; fileRef = {fid} /* {f} */{settings}; }};')
    embed_file_id = uid()
    lines.append(f'\t\t{embed_file_id} /* AdhkarWidgetExtension.appex in Embed App Extensions */ = {{isa = PBXBuildFile; fileRef = {ext_product_id}; settings = {{ATTRIBUTES = (RemoveHeadersOnCopy, ); }}; }};')
    lines.append('/* End PBXBuildFile section */')

    # PBXFileReference
    lines.append('\n/* Begin PBXFileReference section */')
    for f, fid in fref.items():
        name = os.path.basename(f)
        ext = os.path.splitext(f)[1]
        ftype = 'sourcecode.swift' if ext == '.swift' else 'text.plist.xml'
        lines.append(f'\t\t{fid} /* {name} */ = {{isa = PBXFileReference; fileEncoding = 4; lastKnownFileType = {ftype}; name = {name}; path = {f}; sourceTree = SOURCE_ROOT; }};')
    lines.append(f'\t\t{app_product_id} /* AdhkarWidget.app */ = {{isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = AdhkarWidget.app; sourceTree = BUILT_PRODUCTS_DIR; }};')
    lines.append(f'\t\t{ext_product_id} /* AdhkarWidgetExtension.appex */ = {{isa = PBXFileReference; explicitFileType = "wrapper.app-extension"; includeInIndex = 0; path = AdhkarWidgetExtension.appex; sourceTree = BUILT_PRODUCTS_DIR; }};')
    lines.append('/* End PBXFileReference section */')

    # PBXFrameworksBuildPhase
    fw_id = uid()
    ext_fw_id = uid()
    lines.append('\n/* Begin PBXFrameworksBuildPhase section */')
    lines.append(f'\t\t{fw_id} /* Frameworks */ = {{isa = PBXFrameworksBuildPhase; buildActionMask = 2147483647; files = (); runOnlyForDeploymentPostprocessing = 0; }};')
    lines.append(f'\t\t{ext_fw_id} /* Frameworks */ = {{isa = PBXFrameworksBuildPhase; buildActionMask = 2147483647; files = (); runOnlyForDeploymentPostprocessing = 0; }};')
    lines.append('/* End PBXFrameworksBuildPhase section */')

    # PBXGroup (same as before)
    lines.append('\n/* Begin PBXGroup section */')
    lines.append(f'\t\t{products_group_id} /* Products */ = {{isa = PBXGroup; children = ({app_product_id} /* AdhkarWidget.app */, {ext_product_id} /* AdhkarWidgetExtension.appex */,); name = Products; sourceTree = "<group>";}};')
    lines.append(f'\t\t{app_group_id} /* AdhkarWidget */ = {{isa = PBXGroup; children = ({fref["AdhkarWidget/AdhkarWidgetApp.swift"]} /* AdhkarWidgetApp.swift */, {fref["AdhkarWidget/ContentView.swift"]} /* ContentView.swift */, {models_group_id} /* Models */, {widget_group_id} /* Widget */, {fref["AdhkarWidget/Info.plist"]} /* Info.plist */,); name = AdhkarWidget; path = AdhkarWidget; sourceTree = SOURCE_ROOT;}};')
    lines.append(f'\t\t{models_group_id} /* Models */ = {{isa = PBXGroup; children = ({fref["AdhkarWidget/Models/Adhkar.swift"]} /* Adhkar.swift */, {fref["AdhkarWidget/Models/DataStore.swift"]} /* DataStore.swift */, {fref["AdhkarWidget/Models/Views.swift"]} /* Views.swift */,); name = Models; path = Models; sourceTree = SOURCE_ROOT;}};')
    lines.append(f'\t\t{widget_group_id} /* Widget */ = {{isa = PBXGroup; children = ({fref["AdhkarWidget/Widget/AdhkarWidget.swift"]} /* AdhkarWidget.swift */, {fref["AdhkarWidget/Widget/AdhkarWidgetBundle.swift"]} /* AdhkarWidgetBundle.swift */,); name = Widget; path = Widget; sourceTree = SOURCE_ROOT;}};')
    lines.append(f'\t\t{ext_group_id} /* AdhkarWidgetExtension */ = {{isa = PBXGroup; children = ({fref["AdhkarWidgetExtension/Info.plist"]} /* Info.plist */,); name = AdhkarWidgetExtension; path = AdhkarWidgetExtension; sourceTree = SOURCE_ROOT;}};')
    lines.append(f'\t\t{main_group_id} = {{isa = PBXGroup; children = ({app_group_id} /* AdhkarWidget */, {ext_group_id} /* AdhkarWidgetExtension */, {products_group_id} /* Products */,); sourceTree = "<group>";}};')
    lines.append('/* End PBXGroup section */')

    # PBXNativeTarget
    lines.append('\n/* Begin PBXNativeTarget section */')
    lines.append(f'\t\t{app_target_id} /* AdhkarWidget */ = {{isa = PBXNativeTarget; buildConfigurationList = {app_conf_list_id}; buildPhases = ({app_sources_id} /* Sources */, {fw_id} /* Frameworks */, {app_resources_id} /* Resources */, {embed_phase_id} /* Embed App Extensions */,); buildRules = (); dependencies = ({dep_id} /* PBXTargetDependency */,); name = AdhkarWidget; productName = AdhkarWidget; productReference = {app_product_id}; productType = "com.apple.product-type.application";}};')
    lines.append(f'\t\t{ext_target_id} /* AdhkarWidgetExtension */ = {{isa = PBXNativeTarget; buildConfigurationList = {ext_conf_list_id}; buildPhases = ({ext_sources_id} /* Sources */, {ext_fw_id} /* Frameworks */, {ext_resources_id} /* Resources */,); buildRules = (); dependencies = (); name = AdhkarWidgetExtension; productName = AdhkarWidgetExtension; productReference = {ext_product_id}; productType = "com.apple.product-type.app-extension";}};')
    lines.append('/* End PBXNativeTarget section */')

    # PBXProject
    lines.append('\n/* Begin PBXProject section */')
    lines.append(f'\t\t{project_id} /* Project object */ = {{isa = PBXProject; buildConfigurationList = {proj_conf_list_id}; compatibilityVersion = "Xcode 14.0"; developmentRegion = "ar"; hasScannedForEncodings = 0; knownRegions = ("en", "ar", "Base"); mainGroup = {main_group_id}; productRefGroup = {products_group_id}; projectDirPath = ""; projectRoot = ""; targets = ({app_target_id} /* AdhkarWidget */, {ext_target_id} /* AdhkarWidgetExtension */,);}};')
    lines.append('/* End PBXProject section */')

    # PBXResourcesBuildPhase
    lines.append('\n/* Begin PBXResourcesBuildPhase section */')
    lines.append(f'\t\t{app_resources_id} /* Resources */ = {{isa = PBXResourcesBuildPhase; buildActionMask = 2147483647; files = (); runOnlyForDeploymentPostprocessing = 0;}};')
    lines.append(f'\t\t{ext_resources_id} /* Resources */ = {{isa = PBXResourcesBuildPhase; buildActionMask = 2147483647; files = (); runOnlyForDeploymentPostprocessing = 0;}};')
    lines.append('/* End PBXResourcesBuildPhase section */')

    # PBXCopyFilesBuildPhase (Embed)
    lines.append('\n/* Begin PBXCopyFilesBuildPhase section */')
    lines.append(f'\t\t{embed_phase_id} /* Embed App Extensions */ = {{isa = PBXCopyFilesBuildPhase; buildActionMask = 2147483647; dstPath = ""; dstSubfolderSpec = 13; files = ({embed_file_id} /* AdhkarWidgetExtension.appex in Embed App Extensions */,); name = "Embed App Extensions"; runOnlyForDeploymentPostprocessing = 0;}};')
    lines.append('/* End PBXCopyFilesBuildPhase section */')

    # PBXSourcesBuildPhase
    lines.append('\n/* Begin PBXSourcesBuildPhase section */')
    lines.append(f'\t\t{app_sources_id} /* Sources */ = {{isa = PBXSourcesBuildPhase; buildActionMask = 2147483647; files = (' + ''.join([f'{bref[f]} /* {os.path.basename(f)} in Sources */, ' for f in src_files]) + '); runOnlyForDeploymentPostprocessing = 0;}};')
    lines.append(f'\t\t{ext_sources_id} /* Sources */ = {{isa = PBXSourcesBuildPhase; buildActionMask = 2147483647; files = (' + ''.join([f'{bref[f]} /* {os.path.basename(f)} in Sources */, ' for f in ext_files]) + '); runOnlyForDeploymentPostprocessing = 0;}};')
    lines.append('/* End PBXSourcesBuildPhase section */')

    # PBXTargetDependency
    proxy_id = uid()
    lines.append('\n/* Begin PBXTargetDependency section */')
    lines.append(f'\t\t{dep_id} /* PBXTargetDependency */ = {{isa = PBXTargetDependency; target = {ext_target_id} /* AdhkarWidgetExtension */; targetProxy = {proxy_id};}};')
    lines.append('/* End PBXTargetDependency section */')

    # PBXContainerItemProxy
    lines.append('\n/* Begin PBXContainerItemProxy section */')
    lines.append(f'\t\t{proxy_id} /* PBXContainerItemProxy */ = {{isa = PBXContainerItemProxy; containerPortal = {project_id} /* Project object */; proxyType = 1; remoteGlobalIDString = {ext_target_id}; remoteInfo = AdhkarWidgetExtension;}};')
    lines.append('/* End PBXContainerItemProxy section */')

    # XCBuildConfiguration
    lines.append('\n/* Begin XCBuildConfiguration section */')
    # App Debug
    lines.append(f'\t\t{app_debug_id} /* Debug */ = {{isa = XCBuildConfiguration; buildSettings = {{ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon; CODE_SIGN_IDENTITY = "-"; CODE_SIGN_STYLE = Manual; CURRENT_PROJECT_VERSION = 1; INFOPLIST_FILE = "AdhkarWidget/Info.plist"; IPHONEOS_DEPLOYMENT_TARGET = "17.0"; MARKETING_VERSION = "1.0"; PRODUCT_BUNDLE_IDENTIFIER = "com.adhkar.widgetapp"; PRODUCT_NAME = "$(TARGET_NAME)"; SWIFT_VERSION = "5.0"; TARGETED_DEVICE_FAMILY = "1"; GENERATE_INFOPLIST_FILE = NO;}}; name = Debug;}};')
    # App Release
    lines.append(f'\t\t{app_release_id} /* Release */ = {{isa = XCBuildConfiguration; buildSettings = {{ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon; CODE_SIGN_IDENTITY = "-"; CODE_SIGN_STYLE = Manual; CURRENT_PROJECT_VERSION = 1; INFOPLIST_FILE = "AdhkarWidget/Info.plist"; IPHONEOS_DEPLOYMENT_TARGET = "17.0"; MARKETING_VERSION = "1.0"; PRODUCT_BUNDLE_IDENTIFIER = "com.adhkar.widgetapp"; PRODUCT_NAME = "$(TARGET_NAME)"; SWIFT_VERSION = "5.0"; TARGETED_DEVICE_FAMILY = "1"; GENERATE_INFOPLIST_FILE = NO;}}; name = Release;}};')
    # Ext Debug
    lines.append(f'\t\t{ext_debug_id} /* Debug */ = {{isa = XCBuildConfiguration; buildSettings = {{CODE_SIGN_IDENTITY = "-"; CODE_SIGN_STYLE = Manual; CURRENT_PROJECT_VERSION = 1; INFOPLIST_FILE = "AdhkarWidgetExtension/Info.plist"; IPHONEOS_DEPLOYMENT_TARGET = "17.0"; MARKETING_VERSION = "1.0"; PRODUCT_BUNDLE_IDENTIFIER = "com.adhkar.widgetapp.extension"; PRODUCT_NAME = "$(TARGET_NAME)"; SKIP_INSTALL = YES; SWIFT_VERSION = "5.0"; GENERATE_INFOPLIST_FILE = NO;}}; name = Debug;}};')
    # Ext Release
    lines.append(f'\t\t{ext_release_id} /* Release */ = {{isa = XCBuildConfiguration; buildSettings = {{CODE_SIGN_IDENTITY = "-"; CODE_SIGN_STYLE = Manual; CURRENT_PROJECT_VERSION = 1; INFOPLIST_FILE = "AdhkarWidgetExtension/Info.plist"; IPHONEOS_DEPLOYMENT_TARGET = "17.0"; MARKETING_VERSION = "1.0"; PRODUCT_BUNDLE_IDENTIFIER = "com.adhkar.widgetapp.extension"; PRODUCT_NAME = "$(TARGET_NAME)"; SKIP_INSTALL = YES; SWIFT_VERSION = "5.0"; GENERATE_INFOPLIST_FILE = NO;}}; name = Release;}};')
    # Project Debug
    lines.append(f'\t\t{proj_debug_cid} /* Debug */ = {{isa = XCBuildConfiguration; buildSettings = {{ALWAYS_SEARCH_USER_PATHS = NO; CLANG_ANALYZER_NONNULL = YES; CLANG_CXX_LANGUAGE_STANDARD = "gnu++14"; CLANG_ENABLE_MODULES = YES; CLANG_ENABLE_OBJC_ARC = YES; COPY_PHASE_STRIP = NO; ENABLE_STRICT_OBJC_MSGSEND = YES; GCC_OPTIMIZATION_LEVEL = 0; GCC_PREPROCESSOR_DEFINITIONS = ("DEBUG=1", "$(inherited)"); IPHONEOS_DEPLOYMENT_TARGET = "17.0"; MTL_ENABLE_DEBUG_INFO = INCLUDE_SOURCE; ONLY_ACTIVE_ARCH = YES; SDKROOT = iphoneos; SWIFT_ACTIVE_COMPILATION_CONDITIONS = "DEBUG"; SWIFT_OPTIMIZATION_LEVEL = "-Onone";}}; name = Debug;}};')
    # Project Release
    lines.append(f'\t\t{proj_release_cid} /* Release */ = {{isa = XCBuildConfiguration; buildSettings = {{ALWAYS_SEARCH_USER_PATHS = NO; CLANG_ANALYZER_NONNULL = YES; CLANG_CXX_LANGUAGE_STANDARD = "gnu++14"; CLANG_ENABLE_MODULES = YES; CLANG_ENABLE_OBJC_ARC = YES; COPY_PHASE_STRIP = NO; ENABLE_NS_ASSERTIONS = NO; ENABLE_STRICT_OBJC_MSGSEND = YES; GCC_OPTIMIZATION_LEVEL = s; IPHONEOS_DEPLOYMENT_TARGET = "17.0"; MTL_ENABLE_DEBUG_INFO = NO; SDKROOT = iphoneos; SWIFT_COMPILATION_MODE = wholemodule; SWIFT_OPTIMIZATION_LEVEL = "-O"; VALIDATE_PRODUCT = YES;}}; name = Release;}};')
    lines.append('/* End XCBuildConfiguration section */')

    # XCConfigurationList
    lines.append('\n/* Begin XCConfigurationList section */')
    lines.append(f'\t\t{app_conf_list_id} /* App */ = {{isa = XCConfigurationList; buildConfigurations = ({app_debug_id} /* Debug */, {app_release_id} /* Release */,); defaultConfigurationIsVisible = 0; defaultConfigurationName = Release;}};')
    lines.append(f'\t\t{ext_conf_list_id} /* Extension */ = {{isa = XCConfigurationList; buildConfigurations = ({ext_debug_id} /* Debug */, {ext_release_id} /* Release */,); defaultConfigurationIsVisible = 0; defaultConfigurationName = Release;}};')
    lines.append(f'\t\t{proj_conf_list_id} /* Project */ = {{isa = XCConfigurationList; buildConfigurations = ({proj_debug_cid} /* Debug */, {proj_release_cid} /* Release */,); defaultConfigurationIsVisible = 0; defaultConfigurationName = Release;}};')
    lines.append('/* End XCConfigurationList section */')

    # Close
    lines.append('\t};')
    lines.append(f'\trootObject = {project_id};')
    lines.append('}')

    # Write pbxproj
    os.makedirs('AdhkarWidget.xcodeproj', exist_ok=True)
    with open('AdhkarWidget.xcodeproj/project.pbxproj', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    # Create shared scheme
    os.makedirs('AdhkarWidget.xcodeproj/xcshareddata/xcschemes', exist_ok=True)
    scheme_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<Scheme
   LastUpgradeVersion = "1540"
   version = "1.7">
   <BuildAction
      parallelizeBuildables = "YES"
      buildImplicitDependencies = "YES">
      <BuildActionEntries>
         <BuildActionEntry
            buildForTesting = "YES"
            buildForRunning = "YES"
            buildForProfiling = "YES"
            buildForArchiving = "YES"
            buildForAnalyzing = "YES">
            <BuildableReference
               BuildableIdentifier = "primary"
               BlueprintIdentifier = "{app_target_id}"
               BuildableName = "AdhkarWidget.app"
               BlueprintName = "AdhkarWidget"
               ReferencedContainer = "container:AdhkarWidget.xcodeproj">
            </BuildableReference>
         </BuildActionEntry>
         <BuildActionEntry
            buildForTesting = "YES"
            buildForRunning = "YES"
            buildForProfiling = "YES"
            buildForArchiving = "YES"
            buildForAnalyzing = "YES">
            <BuildableReference
               BuildableIdentifier = "primary"
               BlueprintIdentifier = "{ext_target_id}"
               BuildableName = "AdhkarWidgetExtension.appex"
               BlueprintName = "AdhkarWidgetExtension"
               ReferencedContainer = "container:AdhkarWidget.xcodeproj">
            </BuildableReference>
         </BuildActionEntry>
      </BuildActionEntries>
   </BuildAction>
   <LaunchAction
      buildConfiguration = "Debug"
      selectedDebuggerIdentifier = "Xcode.DebuggerFoundation.Debugger.LLDB"
      selectedLauncherIdentifier = "Xcode.DebuggerFoundation.Launcher.LLDB"
      launchStyle = "0"
      useCustomWorkingDirectory = "NO"
      ignoresPersistentStateOnLaunch = "NO"
      debugDocumentVersioning = "YES"
      debugServiceExtension = "internal"
      allowLocationSimulation = "YES">
      <BuildableProductRunnable
         runnableDebuggingMode = "0">
         <BuildableReference
            BuildableIdentifier = "primary"
            BlueprintIdentifier = "{app_target_id}"
            BuildableName = "AdhkarWidget.app"
            BlueprintName = "AdhkarWidget"
            ReferencedContainer = "container:AdhkarWidget.xcodeproj">
         </BuildableReference>
      </BuildableProductRunnable>
   </LaunchAction>
   <ProfileAction
      buildConfiguration = "Release"
      shouldUseLaunchSchemeArgsEnv = "YES"
      savedToolIdentifier = ""
      useCustomWorkingDirectory = "NO"
      debugDocumentVersioning = "YES">
      <BuildableProductRunnable
         runnableDebuggingMode = "0">
         <BuildableReference
            BuildableIdentifier = "primary"
            BlueprintIdentifier = "{app_target_id}"
            BuildableName = "AdhkarWidget.app"
            BlueprintName = "AdhkarWidget"
            ReferencedContainer = "container:AdhkarWidget.xcodeproj">
         </BuildableReference>
      </BuildableProductRunnable>
   </ProfileAction>
   <AnalyzeAction
      buildConfiguration = "Debug">
   </AnalyzeAction>
   <ArchiveAction
      buildConfiguration = "Release"
      revealArchiveInOrganizer = "YES">
   </ArchiveAction>
</Scheme>
'''
    with open('AdhkarWidget.xcodeproj/xcshareddata/xcschemes/AdhkarWidget.xcscheme', 'w', encoding='utf-8') as f:
        f.write(scheme_content)

    print('project.pbxproj and scheme created successfully!')

if __name__ == '__main__':
    write_pbxproj()
