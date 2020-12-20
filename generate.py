#!/usr/bin/env python3

import json
from pathlib import Path

def generateLocalizations():
    with open('./localizations.json') as localizationsJsonFile:
        localizationsJsonFileContent = localizationsJsonFile.read()
        localizationsData = json.loads(localizationsJsonFileContent)

        generateAndroidLocalizations(localizationsData)
        generateDesktopLocalizations(localizationsData)

def generateAndroidLocalizations(localizationsData):
    localizationTranslationFormatter = lambda localizationTranslationKey, localizationTranslationValue: '    <string name="{0}">{1}</string>'.format(localizationTranslationKey, localizationTranslationValue)
    localizationTables = __generatedLocalizationTables(localizationsData, localizationTranslationFormatter)

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

def generateDesktopLocalizations(localizationsData):
    localizationTranslationFormatter = lambda localizationTranslationKey, localizationTranslationValue: '{0} = {1}'.format(localizationTranslationKey, localizationTranslationValue)
    localizationTables = __generatedLocalizationTables(localizationsData, localizationTranslationFormatter)

    localizationTableOutputDirectory = './output/desktop/'
    __ensuresDirectoryExistence(localizationTableOutputDirectory)

    for localizationTableLanguageCode in localizationTables:
        localizationTableTranslations = localizationTables[localizationTableLanguageCode]

        localizationTableFileName = '{0}Messages_{1}.properties'.format(localizationTableOutputDirectory, localizationTableLanguageCode)

        with open(localizationTableFileName, 'w') as localizationTableFile:
            localizationTableOutput = '# WARNING: AUTO GENERATED FILE - DO NOT MODIFY!\n\n'
            localizationTableOutput += '\n'.join(localizationTableTranslations)
            localizationTableFile.writelines(localizationTableOutput)

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

    # TODO: clean output before
    generateLocalizations()
