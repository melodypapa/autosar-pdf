add one integeration test case and implement it
- Extract the BswModuleDescription from `xamples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf`
- To verify the class name is 'BswModuleDescription'
- To verify the package is 'M2::AUTOSARTemplates::BswModuleTemplate::BswOverview'
- To verify the note is 'Root element for the description of a single BSW module or BSW cluster. In case it describes a BSW module, the short name of this element equals the name of the BSW module.
Tags: atp.recommendedPackage=BswModuleDescriptions'
- To verify the bases is 'ARElement, ARObject, AtpBlueprint, AtpBlueprintable, AtpClassifier, AtpFeature, AtpStructureElement, CollectableElement, Identifiable, MultilanguageReferrable, PackageableElement, Referrable'
- To verify the attributes has 'bswModuleDependency, bswModuleDocumentation, expectedEntry, implemented
Entry, internalBehavior, moduleId, providedClientServerEntry, providedData, providedModeGroup, releasedTrigger, requiredClientServerEntry, requiredData, requiredModeGroup, requiredTrigger'
- to verify the attribute type of 'bswModuleDependency' is 'BswModuleDependency'
- to verify the attribute type of 'bswModuleDocumentation' is 'SwComponentDocumentation'
- to verify the attribute type of 'providedClientServerEntry' is 'BswModuleClientServerEntry'
- to verify the attribute type of 'providedModeGroup' is 'ModeDeclarationGroupPrototype'
- to verify the attribute type of 'requiredClientServerEntry' is 'BswModuleClientServerEntry'
- to verify the attribute type of 'requiredModeGroup' is 'ModeDeclarationGroupPrototype'