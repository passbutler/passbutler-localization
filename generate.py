#!/usr/bin/env python3

import json
from pathlib import Path

def generateLocalizations():
    localizationsData = __parseLocalizationFile('./localizations.json')
    __generateAndroidLocalizations(localizationsData)
    __generateDesktopLocalizations(localizationsData)

def __parseLocalizationFile(localizationsFilePath):
    with open(localizationsFilePath) as localizationsJsonFile:
        localizationsJsonFileContent = localizationsJsonFile.read()

        # Preserve line breaks and unicode notation characters as they are
        localizationsJsonFileContent = localizationsJsonFileContent.replace('\\n', '\\\\n')
        localizationsJsonFileContent = localizationsJsonFileContent.replace('\\u', '\\\\u')

        localizationsData = json.loads(localizationsJsonFileContent)

        return localizationsData

def __generateAndroidLocalizations(localizationsData):
    localizationTables = __generatedLocalizationTables(localizationsData, __formatAndroidTranslation)

    localizationTableOutputDirectory = './output/android/'
    __ensuresDirectoryExistence(localizationTableOutputDirectory)

    for localizationTableLanguageCode in localizationTables:
        localizationTableTranslations = localizationTables[localizationTableLanguageCode]

        localizationTableFileName = '{0}strings_{1}.xml'.format(localizationTableOutputDirectory, localizationTableLanguageCode)

        with open(localizationTableFileName, 'w') as localizationTableFile:
            localizationTableOutput = '<!-- WARNING: AUTO GENERATED FILE - DO NOT MODIFY! -->\n\n'
            localizationTableOutput += '<resources>\n'
            localizationTableOutput += '\n'.join(localizationTableTranslations) + '\n'
            localizationTableOutput += '</resources>'
            localizationTableFile.writelines(localizationTableOutput)

def __formatAndroidTranslation(localizationTranslationKey, localizationTranslationValue):
    escapedLocalizationTranslationValue = localizationTranslationValue.replace("'", "\\'")
    return '    <string name="{0}">{1}</string>'.format(localizationTranslationKey, escapedLocalizationTranslationValue)

def __generateDesktopLocalizations(localizationsData):
    localizationTables = __generatedLocalizationTables(localizationsData, __formatDesktopTranslation)

    localizationTableOutputDirectory = './output/desktop/'
    __ensuresDirectoryExistence(localizationTableOutputDirectory)

    for localizationTableLanguageCode in localizationTables:
        localizationTableTranslations = localizationTables[localizationTableLanguageCode]

        localizationTableFileName = '{0}Messages_{1}.properties'.format(localizationTableOutputDirectory, localizationTableLanguageCode)

        with open(localizationTableFileName, 'w') as localizationTableFile:
            localizationTableOutput = '# WARNING: AUTO GENERATED FILE - DO NOT MODIFY!\n\n'
            localizationTableOutput += '\n'.join(localizationTableTranslations)
            localizationTableFile.writelines(localizationTableOutput)

def __formatDesktopTranslation(localizationTranslationKey, localizationTranslationValue):
    return '{0} = {1}'.format(localizationTranslationKey, localizationTranslationValue)

def __generatedLocalizationTables(localizationsData, localizationTranslationFormatter):
    localizationSections = localizationsData['sections']

    generatedLocalizationTables = {}

    for localizationSection in localizationSections:
        sectionName = localizationSection['name']
        sectionLocalizations = localizationSection['localizations']

        for localizationKey in sectionLocalizations:
            localizationValues = sectionLocalizations[localizationKey]

            for localizationLanguageCode in localizationValues:
                localizationTranslationKey = localizationKey
                localizationTranslationValue = localizationValues[localizationLanguageCode]

                formattedLocalizationTranslation = localizationTranslationFormatter(localizationTranslationKey, localizationTranslationValue)
                generatedLocalizationTables.setdefault(localizationLanguageCode, []).append(formattedLocalizationTranslation)

    return generatedLocalizationTables

def __ensuresDirectoryExistence(directoryPath):
    Path(directoryPath).mkdir(parents=True, exist_ok=True)

if __name__ == '__main__':
    print('Generate localization files')
    generateLocalizations()
