#!/usr/bin/env ruby

require 'xcodeproj'

project_path = 'AdhkarWidget.xcodeproj'
project = Xcodeproj::Project.new(project_path)

# --- Targets ---
app_target = project.new_target(:application, 'AdhkarWidget', :ios, 'com.adhkar.widgetapp', deployment_target: '17.0')
ext_target = project.new_target(:app_extension, 'AdhkarWidgetExtension', :ios, 'com.adhkar.widgetapp.extension', deployment_target: '17.0')

# --- Groups ---
group = project.main_group
src = group.new_group('AdhkarWidget', 'AdhkarWidget')
models = src.new_group('Models', 'Models')
widget = src.new_group('Widget', 'Widget')
ext_grp = group.new_group('AdhkarWidgetExtension', 'AdhkarWidgetExtension')

# Helper to add file to source phase
def add_source(target, phase, file_ref)
  build_file = phase.add_file_reference(file_ref)
  build_file
end

# --- App target files ---
app_source_files = [
  src.new_file('AdhkarWidget/AdhkarWidgetApp.swift'),
  src.new_file('AdhkarWidget/ContentView.swift'),
  models.new_file('AdhkarWidget/Models/Adhkar.swift'),
  models.new_file('AdhkarWidget/Models/DataStore.swift'),
  models.new_file('AdhkarWidget/Models/Views.swift'),
]
app_source_files.each { |f| add_source(app_target, app_target.source_build_phase, f) }

# Info.plist for app
app_plist = src.new_file('AdhkarWidget/Info.plist')
app_target.resources_build_phase.add_file_reference(app_plist)

# --- Extension target files ---
ext_source_files = [
  widget.new_file('AdhkarWidget/Widget/AdhkarWidget.swift'),
  widget.new_file('AdhkarWidget/Widget/AdhkarWidgetBundle.swift'),
  models.new_file('AdhkarWidget/Models/Adhkar.swift'),
  models.new_file('AdhkarWidget/Models/DataStore.swift'),
  models.new_file('AdhkarWidget/Models/Views.swift'),
]
ext_source_files.each { |f| add_source(ext_target, ext_target.source_build_phase, f) }

# Info.plist for extension
ext_plist = ext_grp.new_file('AdhkarWidgetExtension/Info.plist')
ext_target.resources_build_phase.add_file_reference(ext_plist)

# --- Build settings ---
app_target.build_configurations.each do |config|
  config.build_settings['INFOPLIST_FILE'] = 'AdhkarWidget/Info.plist'
  config.build_settings['IPHONEOS_DEPLOYMENT_TARGET'] = '17.0'
  config.build_settings['SWIFT_VERSION'] = '5.0'
  config.build_settings['PRODUCT_NAME'] = '$(TARGET_NAME)'
  config.build_settings['CODE_SIGN_STYLE'] = 'Manual'
  config.build_settings['CODE_SIGN_IDENTITY'] = '-'
  config.build_settings['PRODUCT_BUNDLE_IDENTIFIER'] = 'com.adhkar.widgetapp'
end

ext_target.build_configurations.each do |config|
  config.build_settings['INFOPLIST_FILE'] = 'AdhkarWidgetExtension/Info.plist'
  config.build_settings['IPHONEOS_DEPLOYMENT_TARGET'] = '17.0'
  config.build_settings['SWIFT_VERSION'] = '5.0'
  config.build_settings['PRODUCT_NAME'] = '$(TARGET_NAME)'
  config.build_settings['CODE_SIGN_STYLE'] = 'Manual'
  config.build_settings['CODE_SIGN_IDENTITY'] = '-'
  config.build_settings['PRODUCT_BUNDLE_IDENTIFIER'] = 'com.adhkar.widgetapp.extension'
end

# --- Dependency ---
app_target.dependencies.new(ext_target)

# --- Embed extension ---
embed = app_target.new_copy_files_build_phase('Embed App Extensions')
embed.symbol_dst_subfolder_spec = :plug_ins
embed.add_file_reference(ext_target.product_reference)

project.save
puts "Project created: #{project_path}"
