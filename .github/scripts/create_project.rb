#!/usr/bin/env ruby

require 'xcodeproj'

project_path = 'AdhkarWidget.xcodeproj'
project = Xcodeproj::Project.new(project_path)
project.name = 'AdhkarWidget'

# --- Targets ---

# App target
app_target = project.new_target(
  :application,
  'AdhkarWidget',
  :ios,
  'com.adhkar.widgetapp',
  deployment_target: '17.0'
)

# Widget Extension target
ext_target = project.new_target(
  :app_extension,
  'AdhkarWidgetExtension',
  :ios,
  'com.adhkar.widgetapp.extension',
  deployment_target: '17.0'
)

# --- Source Files ---

def add_sources(project, target, dir, file_list)
  Dir.glob(file_list).each do |f|
    file = project.new_file(f)
    target.source_build_phase.add_file_reference(file)
  end
end

# Add main app sources (app target)
add_sources(project, app_target, 'AdhkarWidget', 'AdhkarWidget/AdhkarWidgetApp.swift')
add_sources(project, app_target, 'AdhkarWidget', 'AdhkarWidget/ContentView.swift')
add_sources(project, app_target, 'AdhkarWidget', 'AdhkarWidget/Models/*.swift')

# Widget files for extension target
add_sources(project, ext_target, 'AdhkarWidget', 'AdhkarWidget/Widget/AdhkarWidget.swift')
add_sources(project, ext_target, 'AdhkarWidget', 'AdhkarWidget/Widget/AdhkarWidgetBundle.swift')
add_sources(project, ext_target, 'AdhkarWidget', 'AdhkarWidget/Models/*.swift')
add_sources(project, ext_target, 'AdhkarWidget', 'AdhkarWidget/Widget/AdhkarWidgetExtension/Info.plist')

# --- Info.plists ---
app_target.build_configurations.each do |config|
  config.build_settings['INFOPLIST_FILE'] = 'AdhkarWidget/Info.plist'
  config.build_settings['IPHONEOS_DEPLOYMENT_TARGET'] = '17.0'
  config.build_settings['SWIFT_VERSION'] = '5.9'
  config.build_settings['DEVELOPMENT_TEAM'] = ''
  config.build_settings['CODE_SIGN_STYLE'] = 'Manual'
  config.build_settings['CODE_SIGN_IDENTITY'] = ''
  config.build_settings['PRODUCT_NAME'] = 'AdhkarWidget'
end

ext_target.build_configurations.each do |config|
  config.build_settings['INFOPLIST_FILE'] = 'AdhkarWidgetExtension/Info.plist'
  config.build_settings['IPHONEOS_DEPLOYMENT_TARGET'] = '17.0'
  config.build_settings['SWIFT_VERSION'] = '5.9'
  config.build_settings['DEVELOPMENT_TEAM'] = ''
  config.build_settings['CODE_SIGN_STYLE'] = 'Manual'
  config.build_settings['CODE_SIGN_IDENTITY'] = ''
  config.build_settings['PRODUCT_NAME'] = 'AdhkarWidgetExtension'
end

# --- Dependencies (app depends on extension) ---
app_target.build_configurations.each do |config|
  config.build_settings['TARGETED_DEVICE_FAMILY'] = '1,2'
end

# Wire up the extension as a dependency
app_target.dependencies.new(ext_target)

# Embed the extension
embed_phase = app_target.new_copy_files_build_phase('Embed App Extensions')
embed_phase.symbol_dst_subfolder_spec = :frameworks
ext_target.product_reference.name = 'AdhkarWidgetExtension.appex'
embed_phase.add_file_reference(ext_target.product_reference)

project.save
puts "Project created successfully at #{project_path}"
