# Invalid Attribute Types Report

## Overview

- **Total invalid types**: 425
- **Total invalid references**: 782

### `SwComponent` (25 occurrences)

- **ModeInSwcInstanceRef.context**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingCondition`
  - Kind: `reference`, Multiplicity: `*`
- **EOCExecutableEntityRef.component**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingConstraint::ExecutionOrderConstraint`
  - Kind: `attribute`, Multiplicity: `0..1`
- **EOCEventRef.component**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingConstraint::ExecutionOrderConstraint`
  - Kind: `attribute`, Multiplicity: `0..1`
- **CpSoftwareCluster.swComponent**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SoftwareCluster`
  - Kind: `attribute`, Multiplicity: `*`
- **SwComponentPrototypeAssignment.swComponent**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SoftwareCluster`
  - Kind: `attribute`, Multiplicity: `0..1`
- **ComponentInSystemInstanceRef.target**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::InstanceRefs`
  - Kind: `reference`, Multiplicity: `1`
- **CompositionSwComponentType.component**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Composition`
  - Kind: `attribute`, Multiplicity: `*`
- **TDEventVfb.component**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingDescription::TimingDescription`
  - Kind: `attribute`, Multiplicity: `0..1`
- **TDEventSwc.component**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingDescription::TimingDescription`
  - Kind: `attribute`, Multiplicity: `0..1`
- **DataPrototypeInSystemInstanceRef.context**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::InstanceRefs`
  - Kind: `reference`, Multiplicity: `*`
- **SwcServiceDependencyInSystemInstanceRef.contextSwPrototype**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::InstanceRefs`
  - Kind: `reference`, Multiplicity: `*`
- **ComponentInCompositionInstanceRef.context**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Composition::InstanceRefs`
  - Kind: `reference`, Multiplicity: `*`
- **ComponentInCompositionInstanceRef.target**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Composition::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **PortInCompositionTypeInstanceRef.abstractContext**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Composition::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **PPortInCompositionInstanceRef.context**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Composition::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **RPortInCompositionInstanceRef.context**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Composition::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **InstanceEventInCompositionInstanceRef.contextPrototype**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Composition::InstanceRefs`
  - Kind: `reference`, Multiplicity: `*`
- **InnerDataPrototypeGroupInCompositionInstanceRef.contextSw**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::ImplicitCommunicationBehavior::InstanceRef`
  - Kind: `reference`, Multiplicity: `*`
- **InnerRunnableEntityGroupInCompositionInstanceRef.contextSw**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::ImplicitCommunicationBehavior::InstanceRef`
  - Kind: `reference`, Multiplicity: `*`
- **RunnableEntityInCompositionInstanceRef.contextSw**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::ImplicitCommunicationBehavior::InstanceRef`
  - Kind: `reference`, Multiplicity: `*`
- **VariableDataPrototypeInCompositionInstanceRef.contextSw**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::ImplicitCommunicationBehavior::InstanceRef`
  - Kind: `reference`, Multiplicity: `*`
- **InnerPortGroupInCompositionInstanceRef.context**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Components::InstanceRefs`
  - Kind: `reference`, Multiplicity: `*`
- **SwcToEcuMapping.component**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SWmapping`
  - Kind: `attribute`, Multiplicity: `*`
- **ComponentClustering.clustered**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SWmapping`
  - Kind: `attribute`, Multiplicity: `*`
- **ExecutionTimeConstraint.component**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingConstraint::ExecutionTimeConstraint`
  - Kind: `attribute`, Multiplicity: `0..1`

### `SwcService` (14 occurrences)

- **SwcInternalBehavior.service**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior`
  - Kind: `attribute`, Multiplicity: `*`
- **DiagnosticServiceSwMapping.mappedFlatSwc**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping::ServiceMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticServiceSwMapping.mappedSwc**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping::ServiceMapping`
  - Kind: `attribute`, Multiplicity: `0..1`
- **DiagnosticFimFunctionMapping.mappedFlatSwc**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping::ServiceMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticFimFunctionMapping.mappedSwc**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping::ServiceMapping`
  - Kind: `attribute`, Multiplicity: `0..1`
- **DiagnosticEventPortMapping.swcFlatService**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticEventPortMapping.swcService**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping`
  - Kind: `attribute`, Multiplicity: `0..1`
- **DiagnosticOperationCyclePortMapping.swcFlatService**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticOperationCyclePortMapping.swcService**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping`
  - Kind: `attribute`, Multiplicity: `0..1`
- **DiagnosticEnableConditionPortMapping.swcFlatService**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticEnableConditionPortMapping.swcService**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping`
  - Kind: `attribute`, Multiplicity: `0..1`
- **DiagnosticStorageConditionPortMapping.swcFlatService**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticStorageConditionPortMapping.swcService**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping`
  - Kind: `attribute`, Multiplicity: `0..1`
- **SwcServiceDependencyInSystemInstanceRef.targetSwc**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`

### `MultiLanguageOverview` (11 occurrences)

- **SdgCaption.desc**
  - Package: `M2::MSR::AsamHdo::SpecialData`
  - Kind: `attribute`, Multiplicity: `0..1`
- **Describable.desc**
  - Package: `M2::AUTOSARTemplates::GenericStructure::GeneralTemplateClasses::Identifiable`
  - Kind: `attribute`, Multiplicity: `0..1`
- **Identifiable.desc**
  - Package: `M2::AUTOSARTemplates::GenericStructure::GeneralTemplateClasses::Identifiable`
  - Kind: `attribute`, Multiplicity: `0..1`
- **SwRecordLayoutV.desc**
  - Package: `M2::MSR::DataDictionary::RecordLayout`
  - Kind: `attribute`, Multiplicity: `0..1`
- **SwRecordLayoutGroup.desc**
  - Package: `M2::MSR::DataDictionary::RecordLayout`
  - Kind: `attribute`, Multiplicity: `0..1`
- **CompuScale.desc**
  - Package: `M2::MSR::AsamHdo::ComputationMethod`
  - Kind: `attribute`, Multiplicity: `0..1`
- **ScaleConstr.desc**
  - Package: `M2::MSR::AsamHdo::Constraints::GlobalConstraints`
  - Kind: `attribute`, Multiplicity: `0..1`
- **Modification.change**
  - Package: `M2::MSR::AsamHdo::AdminData`
  - Kind: `attribute`, Multiplicity: `1`
- **Modification.reason**
  - Package: `M2::MSR::AsamHdo::AdminData`
  - Kind: `attribute`, Multiplicity: `0..1`
- **Caption.desc**
  - Package: `M2::MSR::Documentation::BlockElements`
  - Kind: `attribute`, Multiplicity: `0..1`
- **LabeledItem.itemLabel**
  - Package: `M2::MSR::Documentation::BlockElements::ListElements`
  - Kind: `attribute`, Multiplicity: `1`

### `Communication` (11 occurrences)

- **ECUMapping.commController**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::ECUResourceMapping`
  - Kind: `attribute`, Multiplicity: `*`
- **FlexrayTpNode.connector**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::TransportProtocols`
  - Kind: `reference`, Multiplicity: `*`
- **CanTpNode.connector**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::TransportProtocols`
  - Kind: `reference`, Multiplicity: `0..1`
- **LinTpNode.connector**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::TransportProtocols`
  - Kind: `reference`, Multiplicity: `0..1`
- **J1939TpNode.connector**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::TransportProtocols`
  - Kind: `reference`, Multiplicity: `0..1`
- **NmNode.controller**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::NetworkManagement`
  - Kind: `reference`, Multiplicity: `0..1`
- **EcuInstance.commController**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreTopology`
  - Kind: `attribute`, Multiplicity: `*`
- **EcuInstance.connector**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreTopology`
  - Kind: `attribute`, Multiplicity: `*`
- **CommunicationConnector.commController**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreTopology`
  - Kind: `reference`, Multiplicity: `0..1`
- **CommConnectorPort.communication**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreTopology`
  - Kind: `attribute`, Multiplicity: `0..1`
- **IPSecRule.direction**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SecureCommunication`
  - Kind: `attribute`, Multiplicity: `0..1`

### `CompositionSw` (10 occurrences)

- **ExecutionOrderConstraint.base**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingConstraint::ExecutionOrderConstraint`
  - Kind: `reference`, Multiplicity: `0..1`
- **ComponentInCompositionInstanceRef.base**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Composition::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **PortInCompositionTypeInstanceRef.base**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Composition::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **InstanceEventInCompositionInstanceRef.base**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Composition::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **InnerDataPrototypeGroupInCompositionInstanceRef.base**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::ImplicitCommunicationBehavior::InstanceRef`
  - Kind: `reference`, Multiplicity: `0..1`
- **InnerRunnableEntityGroupInCompositionInstanceRef.base**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::ImplicitCommunicationBehavior::InstanceRef`
  - Kind: `reference`, Multiplicity: `0..1`
- **RunnableEntityInCompositionInstanceRef.base**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::ImplicitCommunicationBehavior::InstanceRef`
  - Kind: `reference`, Multiplicity: `0..1`
- **VariableDataPrototypeInCompositionInstanceRef.base**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::ImplicitCommunicationBehavior::InstanceRef`
  - Kind: `reference`, Multiplicity: `0..1`
- **InnerPortGroupInCompositionInstanceRef.base**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Components::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **RootSwCompositionPrototype.software**
  - Package: `M2::AUTOSARTemplates::SystemTemplate`
  - Kind: `attribute`, Multiplicity: `0..1`

### `ApplicationComposite` (10 occurrences)

- **ApplicationCompositeElementInPortInterfaceInstanceRef.contextData**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::PortInterface::InstanceRefs`
  - Kind: `reference`, Multiplicity: `*`
- **ApplicationCompositeElementInPortInterfaceInstanceRef.targetData**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::PortInterface::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **DataPrototypeInSystemInstanceRef.contextData**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::InstanceRefs`
  - Kind: `reference`, Multiplicity: `*`
- **DataPrototypeInSenderReceiverInterfaceInstanceRef.contextData**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Transformer::InstanceRef`
  - Kind: `reference`, Multiplicity: `*`
- **DataPrototypeInClientServerInterfaceInstanceRef.contextData**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Transformer::InstanceRef`
  - Kind: `reference`, Multiplicity: `*`
- **DataPrototypeInPortInterfaceInstanceRef.contextData**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Transformer::InstanceRef`
  - Kind: `reference`, Multiplicity: `*`
- **ApplicationCompositeDataTypeSubElementRef.application**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::PortInterface`
  - Kind: `attribute`, Multiplicity: `0..1`
- **CompositeNetworkRepresentation.leafElementElementInPortInterfaceInstanceRef**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Communication`
  - Kind: `attribute`, Multiplicity: `0..1`
- **ParameterInAtomicSWCTypeInstanceRef.contextData**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior::DataElements::InstanceRefs`
  - Kind: `reference`, Multiplicity: `*`
- **VariableInAtomicSWCTypeInstanceRef.contextData**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior::DataElements::InstanceRefs`
  - Kind: `reference`, Multiplicity: `*`

### `DiagnosticRequest` (9 occurrences)

- **DiagnosticRoutine.requestResult**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::CommonDiagnostics`
  - Kind: `attribute`, Multiplicity: `0..1`
- **DiagnosticRequestDownload.request**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::MemoryByAddress`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticRequestUpload.requestUpload**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::MemoryByAddress`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticRequestEmissionRelatedDTCPermanentStatus.request**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::ObdService::Mode_0x0A_RequestEmissionRelated`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticRequestCurrentPowertrainData.requestCurrent**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::ObdService::Mode_0x01_RequestCurrentPowertrain`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticRequestPowertrainFreezeFrameData.request**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::ObdService::Mode_0x02_RequestPowertrainFreeze`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticRequestControlOfOnBoardDevice.requestControl**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::ObdService::Mode_0x08_RequestControlOfOnBoard`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticRequestVehicleInfo.requestVehicle**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::ObdService::Mode_0x09_RequestVehicleInformation`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticRequestEmissionRelatedDTC.request**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::ObdService::Mode_0x03_0x07_RequestEmission`
  - Kind: `reference`, Multiplicity: `0..1`

### `RootSwComposition` (9 occurrences)

- **ComponentInSystemInstanceRef.context**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **OperationInSystemInstanceRef.context**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **VariableDataPrototypeInSystemInstanceRef.context**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **TriggerInSystemInstanceRef.context**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **PortGroupInSystemInstanceRef.context**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **DataPrototypeInSystemInstanceRef.contextRoot**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **SwcServiceDependencyInSystemInstanceRef.contextRootSw**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **PModeInSystemInstanceRef.context**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **System.rootSoftware**
  - Package: `M2::AUTOSARTemplates::SystemTemplate`
  - Kind: `attribute`, Multiplicity: `0..1`

### `EOCExecutableEntity` (8 occurrences)

- **ExecutionOrderConstraint.orderedElement**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingConstraint::ExecutionOrderConstraint`
  - Kind: `attribute`, Multiplicity: `*`
- **EOCExecutableEntityRefAbstract.directSuccessor**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingConstraint::ExecutionOrderConstraint`
  - Kind: `reference`, Multiplicity: `*`
- **EOCExecutableEntityRefGroup.nestedElement**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingConstraint::ExecutionOrderConstraint`
  - Kind: `reference`, Multiplicity: `*`
- **EOCExecutableEntityRefGroup.successor**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingConstraint::ExecutionOrderConstraint`
  - Kind: `reference`, Multiplicity: `*`
- **EOCExecutableEntityRef.successor**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingConstraint::ExecutionOrderConstraint`
  - Kind: `reference`, Multiplicity: `*`
- **EOCEventRef.successor**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingConstraint::ExecutionOrderConstraint`
  - Kind: `reference`, Multiplicity: `*`
- **SynchronizationPointConstraint.sourceEec**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingConstraint::SynchronizationPointConstraint`
  - Kind: `reference`, Multiplicity: `*`
- **SynchronizationPointConstraint.targetEec**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingConstraint::SynchronizationPointConstraint`
  - Kind: `reference`, Multiplicity: `*`

### `EthernetPhysical` (8 occurrences)

- **CouplingPort.defaultVlan**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `reference`, Multiplicity: `0..1`
- **CouplingPort.vlanModifier**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `reference`, Multiplicity: `0..1`
- **VlanMembership.vlan**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `reference`, Multiplicity: `0..1`
- **CouplingPortRatePolicy.vLan**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `reference`, Multiplicity: `*`
- **DiagnosticComControlSpecificChannel.specificPhysical**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::CommunicationControl`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticComControlClass.allPhysical**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::CommunicationControl`
  - Kind: `reference`, Multiplicity: `*`
- **DiagnosticComControlSubNodeChannel.subNode**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::CommunicationControl`
  - Kind: `reference`, Multiplicity: `0..1`
- **UdpNmCluster.vlan**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::NetworkManagement`
  - Kind: `reference`, Multiplicity: `0..1`

### `AbstractRequiredPort` (8 occurrences)

- **AssemblySwConnector.requesterInstanceRef**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Composition`
  - Kind: `attribute`, Multiplicity: `0..1`
- **PassThroughSwConnector.requiredOuter**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Composition`
  - Kind: `reference`, Multiplicity: `0..1`
- **RPortInCompositionInstanceRef.targetRPortPrototype**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Composition::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **RVariableInAtomicSwcInstanceRef.contextRPortPrototype**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Components::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **RModeInAtomicSwcInstanceRef.contextPortPrototype**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Components::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **RTriggerInAtomicSwcInstanceRef.contextRPortPrototype**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Components::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **ROperationInAtomicSwcInstanceRef.contextRPortPrototype**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Components::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **RModeGroupInAtomicSWCInstanceRef.contextRPortPrototype**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Components::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`

### `AbstractProvidedPort` (7 occurrences)

- **AssemblySwConnector.providerInstanceRef**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Composition`
  - Kind: `attribute`, Multiplicity: `0..1`
- **PassThroughSwConnector.providedOuter**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Composition`
  - Kind: `reference`, Multiplicity: `0..1`
- **PModeInSystemInstanceRef.contextPPortPrototype**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **PPortInCompositionInstanceRef.targetPPortPrototype**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Composition::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **PTriggerInAtomicSwcTypeInstanceRef.contextPPortPrototype**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Components::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **POperationInAtomicSwcInstanceRef.contextPPortPrototype**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Components::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **PModeGroupInAtomicSwcInstanceRef.contextPPortPrototype**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Components::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`

### `AtomicSwComponent` (7 occurrences)

- **ParameterInAtomicSWCTypeInstanceRef.base**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior::DataElements::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **VariableInAtomicSWCTypeInstanceRef.base**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior::DataElements::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **VariableInAtomicSwcInstanceRef.base**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Components::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **RModeInAtomicSwcInstanceRef.base**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Components::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **TriggerInAtomicSwcInstanceRef.base**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Components::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **OperationInAtomicSwcInstanceRef.base**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Components::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`
- **ModeGroupInAtomicSwcInstanceRef.base**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Components::InstanceRefs`
  - Kind: `reference`, Multiplicity: `0..1`

### `MultilanguageLong` (6 occurrences)

- **MultilanguageReferrable.longName**
  - Package: `M2::AUTOSARTemplates::GenericStructure::GeneralTemplateClasses::Identifiable`
  - Kind: `attribute`, Multiplicity: `0..1`
- **AliasNameAssignment.label**
  - Package: `M2::AUTOSARTemplates::CommonStructure::FlatMap`
  - Kind: `attribute`, Multiplicity: `0..1`
- **Note.label**
  - Package: `M2::MSR::Documentation::BlockElements::Note`
  - Kind: `attribute`, Multiplicity: `0..1`
- **ValueGroup.label**
  - Package: `M2::MSR::CalibrationData::CalibrationValue`
  - Kind: `attribute`, Multiplicity: `0..1`
- **Prms.label**
  - Package: `M2::MSR::Documentation::BlockElements::GerneralParameters`
  - Kind: `attribute`, Multiplicity: `0..1`
- **GeneralAnnotation.label**
  - Package: `M2::AUTOSARTemplates::GenericStructure::GeneralTemplateClasses::GeneralAnnotation`
  - Kind: `attribute`, Multiplicity: `0..1`

### `IntegerBit` (6 occurrences)

- **CanControllerConfigurationRequirements.maxNumberOfTimeQuantaPer**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Can::CanTopology`
  - Kind: `attribute`, Multiplicity: `0..1`
- **CanControllerConfigurationRequirements.minNumberOfTimeQuantaPer**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Can::CanTopology`
  - Kind: `attribute`, Multiplicity: `0..1`
- **CanControllerFdConfigurationRequirements.maxNumberOfTimeQuantaPer**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Can::CanTopology`
  - Kind: `attribute`, Multiplicity: `0..1`
- **CanControllerFdConfigurationRequirements.minNumberOfTimeQuantaPer**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Can::CanTopology`
  - Kind: `attribute`, Multiplicity: `0..1`
- **CanControllerXlConfigurationRequirements.maxNumberOfTimeQuantaPer**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Can::CanTopology`
  - Kind: `attribute`, Multiplicity: `0..1`
- **CanControllerXlConfigurationRequirements.minNumberOfTimeQuantaPer**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Can::CanTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `ImplementationData` (6 occurrences)

- **PortDefinedArgumentValue.valueType**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior::PortAPIOptions`
  - Kind: `attribute`, Multiplicity: `0..1`
- **SenderRecRecordElementMapping.implementation**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::DataMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **IndexedArrayElement.implementation**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::DataMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **ImplementationDataType.subElement**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ImplementationDataTypes`
  - Kind: `attribute`, Multiplicity: `*`
- **ImplementationDataTypeElement.subElement**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ImplementationDataTypes`
  - Kind: `attribute`, Multiplicity: `*`
- **RoleBasedDataTypeAssignment.used**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior::ServiceMapping`
  - Kind: `reference`, Multiplicity: `0..1`

### `PostBuildVariant` (6 occurrences)

- **PostBuildVariantCriterionValue.variantCriterion**
  - Package: `M2::AUTOSARTemplates::GenericStructure::VariantHandling`
  - Kind: `reference`, Multiplicity: `1`
- **PredefinedVariant.postBuildVariant**
  - Package: `M2::AUTOSARTemplates::GenericStructure::VariantHandling`
  - Kind: `reference`, Multiplicity: `*`
- **PostBuildVariantCondition.matching**
  - Package: `M2::AUTOSARTemplates::GenericStructure::VariantHandling`
  - Kind: `reference`, Multiplicity: `1`
- **PostBuildVariantCriterionValueSet.postBuildVariant**
  - Package: `M2::AUTOSARTemplates::GenericStructure::VariantHandling`
  - Kind: `attribute`, Multiplicity: `*`
- **FMFeatureMapElement.postBuildVariant**
  - Package: `M2::AUTOSARTemplates::FeatureModelTemplate`
  - Kind: `reference`, Multiplicity: `*`
- **VariationPointProxy.postBuildValue**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior::VariantHandling`
  - Kind: `reference`, Multiplicity: `0..1`

### `DiagnosticFunction` (6 occurrences)

- **CpSwClusterResourceToDiagFunctionIdMapping.function**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping::CpSoftwareCluster`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticFimFunctionMapping.mapped**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping::ServiceMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticInhibitSourceEventMapping.inhibitionSource**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping::FimMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticIumprToFunctionIdentifierMapping.function**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticFunctionIdentifierInhibit.function**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Fim`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticFunctionIdentifierInhibit.inhibitSource**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Fim`
  - Kind: `attribute`, Multiplicity: `*`

### `CryptoService` (6 occurrences)

- **DiagnosticAuthTransmitCertificateMapping.cryptoService**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping`
  - Kind: `reference`, Multiplicity: `*`
- **CryptoServiceCertificate.nextHigher**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SecureCommunication`
  - Kind: `reference`, Multiplicity: `0..1`
- **TlsCryptoCipherSuite.certificate**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SecureCommunication`
  - Kind: `reference`, Multiplicity: `0..1`
- **TlsCryptoCipherSuite.remote**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SecureCommunication`
  - Kind: `reference`, Multiplicity: `0..1`
- **IPSecRule.localCertificate**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SecureCommunication`
  - Kind: `reference`, Multiplicity: `*`
- **IPSecRule.remote**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SecureCommunication`
  - Kind: `reference`, Multiplicity: `*`

### `AbstractImplementation` (6 occurrences)

- **ImplementationDataTypeElementInPortInterfaceRef.context**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Transformer::InstanceRef`
  - Kind: `reference`, Multiplicity: `*`
- **ImplementationElementInParameterInstanceRef.target**
  - Package: `M2::AUTOSARTemplates::CommonStructure::MeasurementCalibrationSupport`
  - Kind: `reference`, Multiplicity: `0..1`
- **ArVariableInImplementationDataInstanceRef.contextData**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior::DataElements`
  - Kind: `reference`, Multiplicity: `*`
- **ArVariableInImplementationDataInstanceRef.targetData**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior::DataElements`
  - Kind: `reference`, Multiplicity: `0..1`
- **ArParameterInImplementationDataInstanceRef.contextData**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior::DataElements`
  - Kind: `reference`, Multiplicity: `*`
- **ArParameterInImplementationDataInstanceRef.targetData**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior::DataElements`
  - Kind: `reference`, Multiplicity: `0..1`

### `ParameterData` (5 occurrences)

- **SwcInternalBehavior.perInstance**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior`
  - Kind: `attribute`, Multiplicity: `*`
- **SwcInternalBehavior.shared**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior`
  - Kind: `attribute`, Multiplicity: `*`
- **BswInternalBehavior.perInstance**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `attribute`, Multiplicity: `*`
- **ArParameterInImplementationDataInstanceRef.rootParameter**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior::DataElements`
  - Kind: `reference`, Multiplicity: `0..1`
- **InternalBehavior.constant**
  - Package: `M2::AUTOSARTemplates::CommonStructure::InternalBehavior`
  - Kind: `attribute`, Multiplicity: `*`

### `SecureCommunication` (5 occurrences)

- **SecuredIPdu.authentication**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreCommunication`
  - Kind: `reference`, Multiplicity: `0..1`
- **SecuredIPdu.freshnessProps**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreCommunication`
  - Kind: `reference`, Multiplicity: `0..1`
- **SecuredIPdu.secure**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreCommunication`
  - Kind: `attribute`, Multiplicity: `0..1`
- **SecureCommunicationPropsSet.authentication**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreCommunication`
  - Kind: `attribute`, Multiplicity: `*`
- **SecureCommunicationPropsSet.freshnessProps**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreCommunication`
  - Kind: `attribute`, Multiplicity: `*`

### `BswService` (5 occurrences)

- **BswInternalBehavior.service**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `attribute`, Multiplicity: `*`
- **BswServiceDependency.ident**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `attribute`, Multiplicity: `0..1`
- **DiagnosticServiceSwMapping.mappedBsw**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping::ServiceMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticFimFunctionMapping.mappedBsw**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping::ServiceMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticEventPortMapping.bswService**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping`
  - Kind: `reference`, Multiplicity: `0..1`

### `ExclusiveAreaNesting` (5 occurrences)

- **BswDirectCallPoint.calledFrom**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `reference`, Multiplicity: `0..1`
- **BswSynchronousServerCallPoint.calledFrom**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `reference`, Multiplicity: `0..1`
- **SynchronousServerCallPoint.calledFrom**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior::ServerCall`
  - Kind: `reference`, Multiplicity: `0..1`
- **InternalBehavior.exclusiveAreaNesting**
  - Package: `M2::AUTOSARTemplates::CommonStructure::InternalBehavior`
  - Kind: `attribute`, Multiplicity: `*`
- **ExecutableEntity.exclusiveAreaNesting**
  - Package: `M2::AUTOSARTemplates::CommonStructure::InternalBehavior`
  - Kind: `reference`, Multiplicity: `*`

### `BswModuleClientServer` (5 occurrences)

- **BswSynchronousServerCallPoint.calledEntryEntry**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `reference`, Multiplicity: `0..1`
- **BswAsynchronousServerCallPoint.calledEntryEntry**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `reference`, Multiplicity: `0..1`
- **BswOperationInvokedEvent.entry**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `reference`, Multiplicity: `0..1`
- **BswModuleDescription.providedClient**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswOverview`
  - Kind: `attribute`, Multiplicity: `*`
- **BswModuleDescription.requiredClient**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswOverview`
  - Kind: `attribute`, Multiplicity: `*`

### `SecurityEventContext` (5 occurrences)

- **DiagnosticSecurityEventReportingModeMapping.securityEventContext**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping::ServiceMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticEventToSecurityEventMapping.securityEventContext**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **SecurityEventContextProps.contextData**
  - Package: `M2::AUTOSARTemplates::SecurityExtractTemplate`
  - Kind: `attribute`, Multiplicity: `0..1`
- **SecurityEventAggregationFilter.contextData**
  - Package: `M2::AUTOSARTemplates::SecurityExtractTemplate`
  - Kind: `attribute`, Multiplicity: `0..1`
- **SecurityEventContextMapping.mappedSecurity**
  - Package: `M2::AUTOSARTemplates::SecurityExtractTemplate`
  - Kind: `attribute`, Multiplicity: `*`

### `DiagnosticFimAlias` (5 occurrences)

- **DiagnosticFimAliasEventGroupMapping.aliasEvent**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping::FimMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticFimAliasEventMapping.aliasEventEvent**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticEvent`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticFunctionInhibitSource.event**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Fim`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticFunctionInhibitSource.eventGroup**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Fim`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticFimAliasEventGroup.groupedAlias**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Fim`
  - Kind: `reference`, Multiplicity: `*`

### `RoleBasedMcData` (5 occurrences)

- **RptComponent.mcData**
  - Package: `M2::AUTOSARTemplates::CommonStructure::MeasurementCalibrationSupport::RptSupport`
  - Kind: `attribute`, Multiplicity: `*`
- **RptExecutableEntity.rptRead**
  - Package: `M2::AUTOSARTemplates::CommonStructure::MeasurementCalibrationSupport::RptSupport`
  - Kind: `attribute`, Multiplicity: `*`
- **RptExecutableEntity.rptWrite**
  - Package: `M2::AUTOSARTemplates::CommonStructure::MeasurementCalibrationSupport::RptSupport`
  - Kind: `attribute`, Multiplicity: `*`
- **RptExecutableEntityEvent.mcData**
  - Package: `M2::AUTOSARTemplates::CommonStructure::MeasurementCalibrationSupport::RptSupport`
  - Kind: `attribute`, Multiplicity: `*`
- **McDataInstance.mcData**
  - Package: `M2::AUTOSARTemplates::CommonStructure::MeasurementCalibrationSupport`
  - Kind: `attribute`, Multiplicity: `*`

### `SwcToSwcOperation` (5 occurrences)

- **CommonSignalPath.operation**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SignalPaths`
  - Kind: `attribute`, Multiplicity: `*`
- **SwcToSwcOperationArguments.direction**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SignalPaths`
  - Kind: `attribute`, Multiplicity: `0..1`
- **ForbiddenSignalPath.operation**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SignalPaths`
  - Kind: `attribute`, Multiplicity: `*`
- **PermissibleSignalPath.operation**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SignalPaths`
  - Kind: `attribute`, Multiplicity: `*`
- **SeparateSignalPath.operation**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SignalPaths`
  - Kind: `attribute`, Multiplicity: `*`

### `AutosarOperation` (4 occurrences)

- **TimingConditionFormula.timingArgumentArgumentInstance**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingCondition`
  - Kind: `reference`, Multiplicity: `0..1`
- **TimingExtensionResource.timingArgument**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingCondition`
  - Kind: `attribute`, Multiplicity: `*`
- **TDEventOccurrenceExpression.argument**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingDescription::TimingDescription`
  - Kind: `attribute`, Multiplicity: `*`
- **TDEventOccurrenceExpressionFormula.argument**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingDescription::TimingDescription`
  - Kind: `reference`, Multiplicity: `0..1`

### `AutosarVariable` (4 occurrences)

- **TimingConditionFormula.timingVariableInstance**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingCondition`
  - Kind: `reference`, Multiplicity: `0..1`
- **TimingExtensionResource.timingVariable**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingCondition`
  - Kind: `attribute`, Multiplicity: `*`
- **TDEventOccurrenceExpression.variable**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingDescription::TimingDescription`
  - Kind: `attribute`, Multiplicity: `*`
- **TDEventOccurrenceExpressionFormula.variable**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingDescription::TimingDescription`
  - Kind: `reference`, Multiplicity: `0..1`

### `SenderRecComposite` (4 occurrences)

- **SenderReceiverToSignalGroupMapping.typeMapping**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::DataMapping`
  - Kind: `attribute`, Multiplicity: `0..1`
- **SenderRecRecordElementMapping.complexType**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::DataMapping`
  - Kind: `attribute`, Multiplicity: `0..1`
- **SenderRecArrayElementMapping.complexType**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::DataMapping`
  - Kind: `attribute`, Multiplicity: `0..1`
- **SenderReceiverCompositeElementToSignalMapping.typeMapping**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::DataMapping`
  - Kind: `attribute`, Multiplicity: `0..1`

### `AutosarEngineering` (4 occurrences)

- **AclObjectSet.engineering**
  - Package: `M2::AUTOSARTemplates::GenericStructure::RolesAndRights`
  - Kind: `attribute`, Multiplicity: `*`
- **Code.artifact**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Implementation`
  - Kind: `attribute`, Multiplicity: `*`
- **DependencyOnArtifact.artifact**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Implementation`
  - Kind: `attribute`, Multiplicity: `0..1`
- **BuildActionEntity.deliveryArtifact**
  - Package: `M2::AUTOSARTemplates::GenericStructure::BuildActionManifest`
  - Kind: `attribute`, Multiplicity: `*`

### `BswDistinguished` (4 occurrences)

- **BswInternalBehavior.distinguished**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `attribute`, Multiplicity: `*`
- **BswModuleCallPoint.context**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `reference`, Multiplicity: `*`
- **BswVariableAccess.context**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `reference`, Multiplicity: `*`
- **BswEvent.context**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `reference`, Multiplicity: `*`

### `DiagnosticOperation` (4 occurrences)

- **DiagnosticAging.agingCycle**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticAging`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticEventToOperationCycleMapping.operationCycle**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticOperationCyclePortMapping.operationCycle**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticOperationCycle.typeCycleTypeEnum**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticOperationCycle`
  - Kind: `attribute`, Multiplicity: `0..1`

### `ArraySizeSemantics` (4 occurrences)

- **DiagnosticDataElement.arraySize**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::CommonDiagnostics`
  - Kind: `attribute`, Multiplicity: `0..1`
- **ImplementationDataTypeElement.arraySize**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ImplementationDataTypes`
  - Kind: `attribute`, Multiplicity: `0..1`
- **SwTextProps.arraySize**
  - Package: `M2::MSR::DataDictionary::DataDefProperties`
  - Kind: `attribute`, Multiplicity: `0..1`
- **ApplicationArrayElement.arraySize**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Datatype::DataPrototypes`
  - Kind: `attribute`, Multiplicity: `0..1`

### `FMConditionByFeatures` (4 occurrences)

- **FMFeatureRestriction.restrictionAndAttributes**
  - Package: `M2::AUTOSARTemplates::FeatureModelTemplate`
  - Kind: `attribute`, Multiplicity: `0..1`
- **FMFeatureRelation.restriction**
  - Package: `M2::AUTOSARTemplates::FeatureModelTemplate`
  - Kind: `attribute`, Multiplicity: `0..1`
- **FMFeatureMapCondition.fmCondAndAttributes**
  - Package: `M2::AUTOSARTemplates::FeatureModelTemplate`
  - Kind: `attribute`, Multiplicity: `0..1`
- **FMFeatureMapAssertion.fmSyscondAndSwSystemconsts**
  - Package: `M2::AUTOSARTemplates::FeatureModelTemplate`
  - Kind: `attribute`, Multiplicity: `0..1`

### `ApplicationPrimitive` (4 occurrences)

- **SwDataDefProps.valueAxisData**
  - Package: `M2::MSR::DataDictionary::DataDefProperties`
  - Kind: `reference`, Multiplicity: `0..1`
- **ApplicationArrayElement.indexDataType**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Datatype::DataPrototypes`
  - Kind: `reference`, Multiplicity: `0..1`
- **SwAxisIndividual.inputVariable**
  - Package: `M2::MSR::DataDictionary::Axis`
  - Kind: `reference`, Multiplicity: `0..1`
- **SwAxisGrouped.sharedAxisType**
  - Package: `M2::MSR::DataDictionary::Axis`
  - Kind: `reference`, Multiplicity: `0..1`

### `EcucAbstractReference` (4 occurrences)

- **EcucContainerValue.referenceValue**
  - Package: `M2::AUTOSARTemplates::ECUCDescriptionTemplate`
  - Kind: `attribute`, Multiplicity: `*`
- **EcucAbstractReferenceValue.definition**
  - Package: `M2::AUTOSARTemplates::ECUCDescriptionTemplate`
  - Kind: `reference`, Multiplicity: `0..1`
- **EcucParamConfContainerDef.reference**
  - Package: `M2::AUTOSARTemplates::ECUCParameterDefTemplate`
  - Kind: `attribute`, Multiplicity: `*`
- **EcucDestinationUriPolicy.reference**
  - Package: `M2::AUTOSARTemplates::ECUCParameterDefTemplate`
  - Kind: `attribute`, Multiplicity: `*`

### `SignalService` (4 occurrences)

- **SignalServiceTranslationProps.serviceControl**
  - Package: `M2::AUTOSARTemplates::CommonStructure::SignalServiceTranslation`
  - Kind: `attribute`, Multiplicity: `0..1`
- **SignalServiceTranslationProps.signalServiceEventProps**
  - Package: `M2::AUTOSARTemplates::CommonStructure::SignalServiceTranslation`
  - Kind: `attribute`, Multiplicity: `*`
- **SignalServiceTranslationPropsSet.signalServiceProps**
  - Package: `M2::AUTOSARTemplates::CommonStructure::SignalServiceTranslation`
  - Kind: `attribute`, Multiplicity: `*`
- **SignalServiceTranslationEventProps.elementProps**
  - Package: `M2::AUTOSARTemplates::CommonStructure::SignalServiceTranslation`
  - Kind: `attribute`, Multiplicity: `*`

### `BooleanEnabled` (4 occurrences)

- **NmEcu.nmBusSynchronization**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::NetworkManagement`
  - Kind: `attribute`, Multiplicity: `0..1`
- **NmEcu.nmPduRxIndication**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::NetworkManagement`
  - Kind: `attribute`, Multiplicity: `0..1`
- **NmEcu.nmRemoteSleepInd**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::NetworkManagement`
  - Kind: `attribute`, Multiplicity: `0..1`
- **CanNmClusterCoupling.nmBusloadReduction**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::NetworkManagement`
  - Kind: `attribute`, Multiplicity: `0..1`

### `AsynchronousServer` (3 occurrences)

- **RunnableEntity.asynchronousServer**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior`
  - Kind: `attribute`, Multiplicity: `*`
- **AsynchronousServerCallResultPoint.asynchronousServer**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior::ServerCall`
  - Kind: `reference`, Multiplicity: `0..1`
- **AsynchronousServerCallReturnsEvent.eventSource**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior::RTEEvents`
  - Kind: `reference`, Multiplicity: `0..1`

### `InstantiationDataDef` (3 occurrences)

- **SwcInternalBehavior.instantiationDataDef**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior`
  - Kind: `attribute`, Multiplicity: `*`
- **NvBlockDescriptor.instantiationDataDef**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::NvBlockComponent`
  - Kind: `attribute`, Multiplicity: `*`
- **ParameterSwComponentType.instantiationDataDef**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Components`
  - Kind: `attribute`, Multiplicity: `*`

### `RoleBasedData` (3 occurrences)

- **NvBlockDescriptor.writingStrategy**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::NvBlockComponent`
  - Kind: `attribute`, Multiplicity: `*`
- **BswServiceDependency.assignedData**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `attribute`, Multiplicity: `*`
- **SwcServiceDependency.assignedData**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior::ServiceMapping`
  - Kind: `attribute`, Multiplicity: `*`

### `HandleOutOfRange` (3 occurrences)

- **ISignalProps.handleOutOfRange**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreCommunication`
  - Kind: `attribute`, Multiplicity: `0..1`
- **ReceiverComSpec.handleOutOfRange**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Communication`
  - Kind: `attribute`, Multiplicity: `0..1`
- **SenderComSpec.handleOutOfRange**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Communication`
  - Kind: `attribute`, Multiplicity: `0..1`

### `TransmissionMode` (3 occurrences)

- **IPduTiming.transmission**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreCommunication`
  - Kind: `attribute`, Multiplicity: `0..1`
- **TransmissionModeDeclaration.transmission**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreCommunication::Timing`
  - Kind: `attribute`, Multiplicity: `0..1`
- **TransmissionComSpecProps.transmission**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Communication`
  - Kind: `attribute`, Multiplicity: `0..1`

### `PduCollectionTrigger` (3 occurrences)

- **ContainedIPduProps.trigger**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreCommunication`
  - Kind: `attribute`, Multiplicity: `0..1`
- **SoConIPduIdentifier.pduCollectionTrigger**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ServiceInstances`
  - Kind: `attribute`, Multiplicity: `0..1`
- **IEEE1722TpAcfBusPart.collectionTrigger**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::TransportProtocols::IEEE1722Tp::IEEE1722TpAcf`
  - Kind: `attribute`, Multiplicity: `0..1`

### `ApplicationRecord` (3 occurrences)

- **SenderRecRecordElementMapping.applicationRecord**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::DataMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **ApplicationRecordDataType.element**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Datatype::Datatypes`
  - Kind: `attribute`, Multiplicity: `*`
- **TlvDataIdDefinition.tlvRecord**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Transformer`
  - Kind: `reference`, Multiplicity: `0..1`

### `SwSystemconstant` (3 occurrences)

- **PredefinedVariant.sw**
  - Package: `M2::AUTOSARTemplates::GenericStructure::VariantHandling`
  - Kind: `reference`, Multiplicity: `*`
- **FMFeatureMapElement.swValueSet**
  - Package: `M2::AUTOSARTemplates::FeatureModelTemplate`
  - Kind: `reference`, Multiplicity: `*`
- **McSupportData.measurable**
  - Package: `M2::AUTOSARTemplates::CommonStructure::MeasurementCalibrationSupport`
  - Kind: `reference`, Multiplicity: `*`

### `BswInternalTriggering` (3 occurrences)

- **BswInternalBehavior.internal**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `attribute`, Multiplicity: `*`
- **BswModuleEntity.activationPoint**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `reference`, Multiplicity: `*`
- **BswInternalTriggerOccurredEvent.eventSourcePoint**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `reference`, Multiplicity: `0..1`

### `DiagnosticAccess` (3 occurrences)

- **DiagnosticServiceInstance.access**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::CommonService`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticRoutineSubfunction.access**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::CommonDiagnostics`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticMemoryIdentifier.access**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::MemoryByAddress`
  - Kind: `reference`, Multiplicity: `0..1`

### `DiagnosticService` (3 occurrences)

- **DiagnosticServiceSwMapping.serviceInstance**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping::ServiceMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticServiceTable.serviceInstance**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticContribution`
  - Kind: `reference`, Multiplicity: `*`
- **DiagnosticCommunicationManagerNeeds.serviceRequest**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ServiceNeeds`
  - Kind: `attribute`, Multiplicity: `0..1`

### `ProvidedService` (3 occurrences)

- **ApplicationEndpoint.providedService**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `*`
- **ConsumedServiceInstance.providedService**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ServiceInstances`
  - Kind: `reference`, Multiplicity: `0..1`
- **ConsumedProvidedServiceInstanceGroup.providedService**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ServiceInstances`
  - Kind: `reference`, Multiplicity: `*`

### `DiagnosticEnable` (3 occurrences)

- **DiagnosticEventToEnableConditionGroupMapping.enableCondition**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticEnableConditionPortMapping.enableCondition**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticEnableConditionGroup.enableCondition**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticConditionGroup`
  - Kind: `reference`, Multiplicity: `*`

### `DiagnosticStorage` (3 occurrences)

- **DiagnosticEventToStorageConditionGroupMapping.storage**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticStorageConditionPortMapping.diagnosticStorage**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticStorageConditionGroup.storage**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticConditionGroup`
  - Kind: `reference`, Multiplicity: `*`

### `CpSoftwareClusterTo` (3 occurrences)

- **CpSoftwareClusterMappingSet.softwareCluster**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SoftwareCluster`
  - Kind: `attribute`, Multiplicity: `*`
- **SystemMapping.softwareCluster**
  - Package: `M2::AUTOSARTemplates::SystemTemplate`
  - Kind: `attribute`, Multiplicity: `*`
- **SystemMapping.swCluster**
  - Package: `M2::AUTOSARTemplates::SystemTemplate`
  - Kind: `attribute`, Multiplicity: `*`

### `PduActivationRouting` (3 occurrences)

- **ConsumedEventGroup.pduActivationRouting**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ServiceInstances`
  - Kind: `attribute`, Multiplicity: `*`
- **AbstractServiceInstance.method**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ServiceInstances`
  - Kind: `attribute`, Multiplicity: `0..1`
- **EventHandler.pduActivationRouting**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ServiceInstances`
  - Kind: `attribute`, Multiplicity: `*`

### `EthernetCommunication` (3 occurrences)

- **SocketAddress.connector**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ServiceInstances`
  - Kind: `reference`, Multiplicity: `0..1`
- **SocketAddress.multicast**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ServiceInstances`
  - Kind: `reference`, Multiplicity: `*`
- **PlatformModuleEthernetEndpointConfiguration.communication**
  - Package: `M2::AUTOSARTemplates::AdaptivePlatform::PlatformModuleDeployment::AdaptiveModule`
  - Kind: `reference`, Multiplicity: `0..1`

### `RuleBasedValue` (3 occurrences)

- **RuleBasedValueCont.ruleBased**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Constants`
  - Kind: `attribute`, Multiplicity: `0..1`
- **RuleBasedAxisCont.ruleBased**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Constants`
  - Kind: `attribute`, Multiplicity: `0..1`
- **NumericalRuleBasedValueSpecification.ruleBased**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Constants`
  - Kind: `attribute`, Multiplicity: `0..1`

### `CalprmAxisCategory` (3 occurrences)

- **RuleBasedAxisCont.category**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Constants`
  - Kind: `attribute`, Multiplicity: `0..1`
- **SwCalprmAxis.category**
  - Package: `M2::MSR::DataDictionary::CalibrationParameter`
  - Kind: `attribute`, Multiplicity: `0..1`
- **SwAxisCont.category**
  - Package: `M2::MSR::CalibrationData::CalibrationValue`
  - Kind: `attribute`, Multiplicity: `0..1`

### `SwCalibrationAccess` (3 occurrences)

- **ModeDeclarationGroupPrototype.swCalibrationAccess**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ModeDeclaration`
  - Kind: `attribute`, Multiplicity: `0..1`
- **SwCalprmAxis.swCalibrationAccess**
  - Package: `M2::MSR::DataDictionary::CalibrationParameter`
  - Kind: `attribute`, Multiplicity: `0..1`
- **SwDataDefProps.swCalibrationAccess**
  - Package: `M2::MSR::DataDictionary::DataDefProperties`
  - Kind: `attribute`, Multiplicity: `0..1`

### `GlobalTimeCrcSupport` (3 occurrences)

- **GlobalTimeCanMaster.crcSecured**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::GlobalTime::CAN`
  - Kind: `attribute`, Multiplicity: `0..1`
- **GlobalTimeEthMaster.crcSecured**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::GlobalTime::ETH`
  - Kind: `attribute`, Multiplicity: `0..1`
- **GlobalTimeFrMaster.crcSecured**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::GlobalTime::FR`
  - Kind: `attribute`, Multiplicity: `0..1`

### `GlobalTimeCrc` (3 occurrences)

- **GlobalTimeCanSlave.crcValidated**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::GlobalTime::CAN`
  - Kind: `attribute`, Multiplicity: `0..1`
- **GlobalTimeEthSlave.crcValidated**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::GlobalTime::ETH`
  - Kind: `attribute`, Multiplicity: `0..1`
- **GlobalTimeFrSlave.crcValidated**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::GlobalTime::FR`
  - Kind: `attribute`, Multiplicity: `0..1`

### `Url` (3 occurrences)

- **Std.url**
  - Package: `M2::MSR::Documentation::TextModel::InlineTextElements`
  - Kind: `attribute`, Multiplicity: `0..1`
- **Xdoc.url**
  - Package: `M2::MSR::Documentation::TextModel::InlineTextElements`
  - Kind: `attribute`, Multiplicity: `0..1`
- **Xfile.url**
  - Package: `M2::MSR::Documentation::TextModel::InlineTextElements`
  - Kind: `attribute`, Multiplicity: `0..1`

### `EcucConfiguration` (3 occurrences)

- **EcucModuleConfigurationValues.implementation**
  - Package: `M2::AUTOSARTemplates::ECUCDescriptionTemplate`
  - Kind: `attribute`, Multiplicity: `0..1`
- **EcucModuleDef.supported**
  - Package: `M2::AUTOSARTemplates::ECUCParameterDefTemplate`
  - Kind: `attribute`, Multiplicity: `*`
- **EcucAbstractConfigurationClass.configVariant**
  - Package: `M2::AUTOSARTemplates::ECUCParameterDefTemplate`
  - Kind: `attribute`, Multiplicity: `0..1`

### `EcucModule` (3 occurrences)

- **EcucValueCollection.ecucValue**
  - Package: `M2::AUTOSARTemplates::ECUCDescriptionTemplate`
  - Kind: `reference`, Multiplicity: `*`
- **BswImplementation.preconfigured**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswImplementation`
  - Kind: `reference`, Multiplicity: `*`
- **BswImplementation.recommended**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswImplementation`
  - Kind: `reference`, Multiplicity: `*`

### `Diagnostic` (3 occurrences)

- **DiagnosticAccessPermission.environmental**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticAuthentication.authentication**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::Authentication`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticTestResult.monitored**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticTestResult`
  - Kind: `reference`, Multiplicity: `0..1`

### `TransformationCom` (3 occurrences)

- **ReceiverComSpec.transformationCom**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Communication`
  - Kind: `attribute`, Multiplicity: `*`
- **ClientComSpec.transformationCom**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Communication`
  - Kind: `attribute`, Multiplicity: `*`
- **ServerComSpec.transformationCom**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Communication`
  - Kind: `attribute`, Multiplicity: `*`

### `SingleLanguageUnit` (3 occurrences)

- **SwValueCont.unitDisplay**
  - Package: `M2::MSR::CalibrationData::CalibrationValue`
  - Kind: `attribute`, Multiplicity: `0..1`
- **SwAxisCont.unitDisplay**
  - Package: `M2::MSR::CalibrationData::CalibrationValue`
  - Kind: `attribute`, Multiplicity: `0..1`
- **Unit.displayName**
  - Package: `M2::MSR::AsamHdo::Units`
  - Kind: `attribute`, Multiplicity: `0..1`

### `IncludedMode` (2 occurrences)

- **SwcInternalBehavior.includedMode**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior`
  - Kind: `attribute`, Multiplicity: `*`
- **BswInternalBehavior.includedMode**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `attribute`, Multiplicity: `*`

### `XmlSpaceEnum` (2 occurrences)

- **Sd.xmlSpace**
  - Package: `M2::MSR::AsamHdo::SpecialData`
  - Kind: `attribute`, Multiplicity: `0..1`
- **WhitespaceControlled.xmlSpace**
  - Package: `M2::MSR::Documentation::TextModel::LanguageDataModel`
  - Kind: `attribute`, Multiplicity: `1`

### `SingleLanguageLong` (2 occurrences)

- **SingleLanguageReferrable.longName1**
  - Package: `M2::AUTOSARTemplates::GenericStructure::GeneralTemplateClasses::Identifiable`
  - Kind: `attribute`, Multiplicity: `0..1`
- **Xref.label1**
  - Package: `M2::MSR::Documentation::TextModel::InlineTextElements`
  - Kind: `attribute`, Multiplicity: `0..1`

### `AbstractCan` (2 occurrences)

- **AbstractCanCommunicationController.canControllerControllerAttributes**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Can::CanTopology`
  - Kind: `attribute`, Multiplicity: `0..1`
- **EthernetCommunicationController.canXlConfig**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `reference`, Multiplicity: `0..1`

### `EventObdReadiness` (2 occurrences)

- **DiagnosticTroubleCodeUds.eventReadiness**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticTroubleCode`
  - Kind: `attribute`, Multiplicity: `0..1`
- **DiagnosticTroubleCodeObd.eventReadiness**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticTroubleCode`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticMemory` (2 occurrences)

- **DiagnosticTroubleCodeProps.diagnosticMemory**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticTroubleCode`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticMemoryAddressableRangeAccess.memoryRange**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::MemoryByAddress`
  - Kind: `reference`, Multiplicity: `*`

### `RoleBasedPort` (2 occurrences)

- **NvBlockDescriptor.clientServerPort**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::NvBlockComponent`
  - Kind: `attribute`, Multiplicity: `*`
- **SwcServiceDependency.assignedPort**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior::ServiceMapping`
  - Kind: `attribute`, Multiplicity: `*`

### `PortDefinedArgument` (2 occurrences)

- **PortAPIOption.portArgValue**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior::PortAPIOptions`
  - Kind: `attribute`, Multiplicity: `*`
- **ClientServerInterfaceToBswModuleEntryBlueprintMapping.portDefinedArgument**
  - Package: `M2::AUTOSARTemplates::CommonStructure::StandardizationTemplate::ClientServerInterfaceToBsw`
  - Kind: `attribute`, Multiplicity: `*`

### `FirewallActionEnum` (2 occurrences)

- **StateDependentFirewall.defaultAction**
  - Package: `M2::AUTOSARTemplates::AdaptivePlatform::PlatformModuleDeployment::Firewall`
  - Kind: `attribute`, Multiplicity: `0..1`
- **FirewallRuleProps.action**
  - Package: `M2::AUTOSARTemplates::AdaptivePlatform::PlatformModuleDeployment::Firewall`
  - Kind: `attribute`, Multiplicity: `0..1`

### `TransformationISignal` (2 occurrences)

- **ISignal.transformationISignal**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreCommunication`
  - Kind: `attribute`, Multiplicity: `*`
- **ISignalGroup.transformationISignal**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreCommunication`
  - Kind: `attribute`, Multiplicity: `*`

### `ApplicationArray` (2 occurrences)

- **IndexedArrayElement.applicationArray**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::DataMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **ApplicationArrayDataType.element**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Datatype::Datatypes`
  - Kind: `attribute`, Multiplicity: `0..1`

### `MultiplicityRestriction` (2 occurrences)

- **ClassTailoring.multiplicity**
  - Package: `M2::AUTOSARTemplates::CommonStructure::StandardizationTemplate::DataExchangePoint::Data`
  - Kind: `attribute`, Multiplicity: `0..1`
- **AttributeTailoring.multiplicity**
  - Package: `M2::AUTOSARTemplates::CommonStructure::StandardizationTemplate::DataExchangePoint::Data`
  - Kind: `attribute`, Multiplicity: `0..1`

### `VariationRestrictionWith` (2 occurrences)

- **ClassTailoring.variation**
  - Package: `M2::AUTOSARTemplates::CommonStructure::StandardizationTemplate::DataExchangePoint::Data`
  - Kind: `attribute`, Multiplicity: `0..1`
- **AttributeTailoring.variation**
  - Package: `M2::AUTOSARTemplates::CommonStructure::StandardizationTemplate::DataExchangePoint::Data`
  - Kind: `attribute`, Multiplicity: `0..1`

### `PrimitiveAttribute` (2 occurrences)

- **PrimitiveAttributeCondition.attribute**
  - Package: `M2::AUTOSARTemplates::CommonStructure::StandardizationTemplate::DataExchangePoint::Data`
  - Kind: `reference`, Multiplicity: `1`
- **PrimitiveAttributeTailoring.subAttribute**
  - Package: `M2::AUTOSARTemplates::CommonStructure::StandardizationTemplate::DataExchangePoint::Data`
  - Kind: `attribute`, Multiplicity: `*`

### `ReferrableSubtypes` (2 occurrences)

- **AclObjectSet.aclObjectClass**
  - Package: `M2::AUTOSARTemplates::GenericStructure::RolesAndRights`
  - Kind: `attribute`, Multiplicity: `*`
- **ReferenceBase.globalElement**
  - Package: `M2::AUTOSARTemplates::GenericStructure::GeneralTemplateClasses::ARPackage`
  - Kind: `attribute`, Multiplicity: `*`

### `BswSchedulerName` (2 occurrences)

- **BswInternalBehavior.schedulerName**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `attribute`, Multiplicity: `*`
- **BswModuleEntity.schedulerName**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `reference`, Multiplicity: `0..1`

### `BswAsynchronous` (2 occurrences)

- **BswAsynchronousServerCallResultPoint.asynchronous**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `reference`, Multiplicity: `0..1`
- **BswAsynchronousServerCallReturnsEvent.eventSource**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `reference`, Multiplicity: `0..1`

### `ConsumedProvided` (2 occurrences)

- **PncMapping.pncConsumed**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::PncMapping`
  - Kind: `reference`, Multiplicity: `*`
- **EcuInstance.associated**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreTopology`
  - Kind: `reference`, Multiplicity: `*`

### `Transformation` (2 occurrences)

- **DataTransformation.transformer**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Transformer`
  - Kind: `reference`, Multiplicity: `*`
- **TransformationISignalProps.transformer**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Transformer`
  - Kind: `reference`, Multiplicity: `0..1`

### `E2EProfileCompatibility` (2 occurrences)

- **EndToEndTransformationComSpecProps.e2eProfile**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Transformer`
  - Kind: `reference`, Multiplicity: `0..1`
- **EndToEndTransformationDescription.e2eProfile**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Transformer`
  - Kind: `reference`, Multiplicity: `0..1`

### `DiagnosticSupportInfo` (2 occurrences)

- **DiagnosticDataIdentifier.supportInfoByte**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::CommonDiagnostics`
  - Kind: `attribute`, Multiplicity: `0..1`
- **DiagnosticParameterIdentifier.supportInfoByte**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::CommonDiagnostics`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticFimEvent` (2 occurrences)

- **DiagnosticInhibitSourceEventMapping.eventGroupGroup**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping::FimMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticFimAliasEventGroupMapping.actualEvent**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping::FimMapping`
  - Kind: `reference`, Multiplicity: `0..1`

### `DiagnosticDebounce` (2 occurrences)

- **DiagnosticCommonProps.debounce**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticCommonProps`
  - Kind: `attribute`, Multiplicity: `*`
- **DiagnosticEventToDebounceAlgorithmMapping.debounce**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping`
  - Kind: `reference`, Multiplicity: `0..1`

### `ArgumentDirection` (2 occurrences)

- **SwServiceArg.direction**
  - Package: `M2::MSR::DataDictionary::ServiceProcessTask`
  - Kind: `attribute`, Multiplicity: `0..1`
- **ArgumentDataPrototype.direction**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::PortInterface`
  - Kind: `attribute`, Multiplicity: `0..1`

### `EthernetMacLayerType` (2 occurrences)

- **CouplingPort.macLayerTypeEnum**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`
- **EthernetCommunicationController.macLayerType**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `EthernetSwitchVlan` (2 occurrences)

- **CouplingPort.receiveActivity**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`
- **VlanMembership.sendActivity**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `EthernetWakeupSleep` (2 occurrences)

- **CouplingPort.wakeupSleep**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `reference`, Multiplicity: `0..1`
- **EthernetWakeupSleepOnDatalineConfigSet.ethernet**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `*`

### `CouplingPortStructural` (2 occurrences)

- **CouplingPortDetails.couplingPort**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `*`
- **CouplingPortScheduler.predecessor**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `reference`, Multiplicity: `*`

### `SwitchFlowMetering` (2 occurrences)

- **CouplingElementSwitchDetails.flowMetering**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `*`
- **SwitchStreamFilterEntry.flowMetering**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `reference`, Multiplicity: `0..1`

### `SwitchAsynchronous` (2 occurrences)

- **CouplingElementSwitchDetails.trafficShaper**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `*`
- **CouplingPortAsynchronousTrafficShaper.trafficShaper**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `reference`, Multiplicity: `0..1`

### `SwitchStreamFilter` (2 occurrences)

- **SwitchStreamIdentification.filterActionDest**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`
- **SwitchStreamFilterActionDestPortModification.modification**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `StreamFilterMAC` (2 occurrences)

- **StreamFilterRuleDataLinkLayer.destinationMac**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`
- **StreamFilterRuleDataLinkLayer.sourceMac**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `StreamFilterIpv6` (2 occurrences)

- **StreamFilterRuleIpTp.destination**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`
- **StreamFilterRuleIpTp.source**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `ConsumedService` (2 occurrences)

- **ApplicationEndpoint.consumedService**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `*`
- **ConsumedProvidedServiceInstanceGroup.consumedService**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ServiceInstances`
  - Kind: `reference`, Multiplicity: `*`

### `TimeSyncServer` (2 occurrences)

- **TimeSynchronization.timeSyncServerConfiguration**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`
- **OrderedMaster.timeSyncServerConfiguration**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `reference`, Multiplicity: `0..1`

### `TimeSyncTechnology` (2 occurrences)

- **TimeSyncClientConfiguration.timeSync**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`
- **TimeSyncServerConfiguration.timeSync**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticEnvMode` (2 occurrences)

- **DiagnosticEnvironmentalCondition.modeElement**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::EnvironmentalCondition`
  - Kind: `attribute`, Multiplicity: `*`
- **DiagnosticEnvModeCondition.modeElement**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::EnvironmentalCondition`
  - Kind: `reference`, Multiplicity: `0..1`

### `DiagnosticAuthTransmit` (2 occurrences)

- **DiagnosticAuthTransmitCertificateMapping.serviceInstance**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticAuthTransmitCertificate.certificate**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::Authentication`
  - Kind: `attribute`, Multiplicity: `*`

### `DiagnosticWriteDataBy` (2 occurrences)

- **DiagnosticSecureCodingMapping.dataIdentifier**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticMapping`
  - Kind: `reference`, Multiplicity: `*`
- **DiagnosticWriteDataByIdentifier.writeClass**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::DataByIdentifier`
  - Kind: `reference`, Multiplicity: `0..1`

### `DiagnosticClearDtc` (2 occurrences)

- **DiagnosticMemoryDestination.clearDtc**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticMemoryDestination`
  - Kind: `attribute`, Multiplicity: `0..1`
- **DtcStatusChangeNotificationNeeds.notificationTime**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ServiceNeeds`
  - Kind: `attribute`, Multiplicity: `0..1`

### `PortElementTo` (2 occurrences)

- **CpSoftwareClusterMappingSet.portElementTo**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SoftwareCluster`
  - Kind: `attribute`, Multiplicity: `*`
- **SystemMapping.portElementTo**
  - Package: `M2::AUTOSARTemplates::SystemTemplate`
  - Kind: `attribute`, Multiplicity: `*`

### `SwcToApplication` (2 occurrences)

- **CpSoftwareClusterMappingSet.swcTo**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SoftwareCluster`
  - Kind: `attribute`, Multiplicity: `*`
- **SystemMapping.swcTo**
  - Package: `M2::AUTOSARTemplates::SystemTemplate`
  - Kind: `attribute`, Multiplicity: `*`

### `SdClientConfig` (2 occurrences)

- **ConsumedEventGroup.sdClientConfig**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ServiceInstances`
  - Kind: `attribute`, Multiplicity: `0..1`
- **ConsumedServiceInstance.sdClientConfig**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ServiceInstances`
  - Kind: `attribute`, Multiplicity: `0..1`

### `SdServerConfig` (2 occurrences)

- **ProvidedServiceInstance.sdServerConfig**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ServiceInstances`
  - Kind: `attribute`, Multiplicity: `0..1`
- **EventHandler.sdServerConfig**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ServiceInstances`
  - Kind: `attribute`, Multiplicity: `0..1`

### `EventGroupControlType` (2 occurrences)

- **PduActivationRoutingGroup.eventGroup**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ServiceInstances`
  - Kind: `attribute`, Multiplicity: `0..1`
- **SoAdRoutingGroup.eventGroup**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ObsoleteModel`
  - Kind: `attribute`, Multiplicity: `0..1`

### `CalibrationParameter` (2 occurrences)

- **CalibrationParameterValueSet.calibration**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::MeasurementAndCalibration::CalibrationParameter`
  - Kind: `attribute`, Multiplicity: `*`
- **RootSwCompositionPrototype.calibration**
  - Package: `M2::AUTOSARTemplates::SystemTemplate`
  - Kind: `reference`, Multiplicity: `*`

### `DiagnosticCommon` (2 occurrences)

- **DiagnosticContributionSet.common**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticContribution`
  - Kind: `attribute`, Multiplicity: `0..1`
- **DiagnosticContributionSet.element**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticContribution`
  - Kind: `reference`, Multiplicity: `*`

### `DiagnosticReadDataBy` (2 occurrences)

- **DiagnosticReadDataByIdentifier.readClass**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::DataByIdentifier`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticReadDataByPeriodicID.readDataClass**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::ReadDataByPeriodicID`
  - Kind: `reference`, Multiplicity: `0..1`

### `ArraySizeHandling` (2 occurrences)

- **ImplementationDataTypeElement.arraySizeHandling**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ImplementationDataTypes`
  - Kind: `attribute`, Multiplicity: `0..1`
- **ApplicationArrayElement.arraySizeHandling**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Datatype::DataPrototypes`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticIndicatorType` (2 occurrences)

- **IndicatorStatusNeeds.typeEnum**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ServiceNeeds`
  - Kind: `attribute`, Multiplicity: `0..1`
- **DiagnosticIndicator.type**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticIndicator`
  - Kind: `attribute`, Multiplicity: `0..1`

### `CanAddressingMode` (2 occurrences)

- **CanFrameTriggering.canAddressing**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Can::CanCommunication`
  - Kind: `attribute`, Multiplicity: `0..1`
- **IEEE1722TpAcfCanPart.canAddressing**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::TransportProtocols::IEEE1722Tp::IEEE1722TpAcf`
  - Kind: `attribute`, Multiplicity: `0..1`

### `CanFrameTxBehavior` (2 occurrences)

- **CanFrameTriggering.canFrameTxBehavior**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Can::CanCommunication`
  - Kind: `attribute`, Multiplicity: `0..1`
- **IEEE1722TpAcfCanPart.canFrameTxBehavior**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::TransportProtocols::IEEE1722Tp::IEEE1722TpAcf`
  - Kind: `attribute`, Multiplicity: `0..1`

### `RuntimeAddress` (2 occurrences)

- **SocketConnection.runtimeIp**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ObsoleteModel`
  - Kind: `attribute`, Multiplicity: `0..1`
- **SocketConnection.runtimePort**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ObsoleteModel`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticRecord` (2 occurrences)

- **DiagnosticExtendedDataRecord.trigger**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticExtendedDataRecord`
  - Kind: `attribute`, Multiplicity: `0..1`
- **DiagnosticFreezeFrame.trigger**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticFreezeFrame`
  - Kind: `attribute`, Multiplicity: `0..1`

### `TDEventOccurrence` (2 occurrences)

- **TDEventOccurrenceExpression.formula**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingDescription::TimingDescription`
  - Kind: `attribute`, Multiplicity: `0..1`
- **TimingDescriptionEvent.occurrence**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingDescription`
  - Kind: `attribute`, Multiplicity: `0..1`

### `TopicContentOrMsr` (2 occurrences)

- **ChapterContent.topicContentOrMsr**
  - Package: `M2::MSR::Documentation::Chapters`
  - Kind: `attribute`, Multiplicity: `0..1`
- **Topic1.topicContentOrMsr**
  - Package: `M2::MSR::Documentation::Chapters`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticConnected` (2 occurrences)

- **DiagnosticEvent.connected**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticEvent`
  - Kind: `attribute`, Multiplicity: `*`
- **DiagnosticConnectedIndicator.behaviorIndicatorBehaviorEnum**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticEvent`
  - Kind: `attribute`, Multiplicity: `0..1`

### `SenderReceiver` (2 occurrences)

- **DataPrototypeInSenderReceiverInterfaceInstanceRef.baseInterface**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Transformer::InstanceRef`
  - Kind: `reference`, Multiplicity: `0..1`
- **PortPrototype.senderReceiver**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Components`
  - Kind: `attribute`, Multiplicity: `*`

### `DiagnosticDynamically` (2 occurrences)

- **DiagnosticDynamicallyDefineDataIdentifier.dynamically**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::DynamicallyDefineDataIdentifier`
  - Kind: `reference`, Multiplicity: `0..1`
- **DiagnosticDynamicallyDefineDataIdentifierClass.subfunction**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::DynamicallyDefineDataIdentifier`
  - Kind: `attribute`, Multiplicity: `*`

### `IEEE1722TpRvfPixel` (2 occurrences)

- **IEEE1722TpRvfConnection.rvfPixelDepth**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::TransportProtocols::IEEE1722Tp::IEEE1722TpAv`
  - Kind: `attribute`, Multiplicity: `0..1`
- **IEEE1722TpRvfConnection.rvfPixelFormat**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::TransportProtocols::IEEE1722Tp::IEEE1722TpAv`
  - Kind: `attribute`, Multiplicity: `0..1`

### `RptEnablerImplType` (2 occurrences)

- **RptImplPolicy.rptEnablerImpl**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::RPTScenario`
  - Kind: `attribute`, Multiplicity: `0..1`
- **RptProfile.stimEnabler**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::RPTScenario`
  - Kind: `attribute`, Multiplicity: `0..1`

### `RptSwPrototyping` (2 occurrences)

- **RptContainer.rptSw**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::RPTScenario`
  - Kind: `attribute`, Multiplicity: `0..1`
- **McDataInstance.resultingRptSw**
  - Package: `M2::AUTOSARTemplates::CommonStructure::MeasurementCalibrationSupport`
  - Kind: `attribute`, Multiplicity: `0..1`

### `EcucMultiplicity` (2 occurrences)

- **EcucContainerDef.multiplicity**
  - Package: `M2::AUTOSARTemplates::ECUCParameterDefTemplate`
  - Kind: `attribute`, Multiplicity: `*`
- **EcucCommonAttributes.multiplicity**
  - Package: `M2::AUTOSARTemplates::ECUCParameterDefTemplate`
  - Kind: `attribute`, Multiplicity: `*`

### `EcucCondition` (2 occurrences)

- **EcucDefinitionElement.ecucCond**
  - Package: `M2::AUTOSARTemplates::ECUCParameterDefTemplate`
  - Kind: `attribute`, Multiplicity: `0..1`
- **EcucEnumerationLiteralDef.ecucCond**
  - Package: `M2::AUTOSARTemplates::ECUCParameterDefTemplate`
  - Kind: `attribute`, Multiplicity: `0..1`

### `EcucDestinationUri` (2 occurrences)

- **EcucDestinationUriDef.destinationUri**
  - Package: `M2::AUTOSARTemplates::ECUCParameterDefTemplate`
  - Kind: `attribute`, Multiplicity: `0..1`
- **EcucDestinationUriPolicy.destinationUri**
  - Package: `M2::AUTOSARTemplates::ECUCParameterDefTemplate`
  - Kind: `attribute`, Multiplicity: `0..1`

### `ArVariableIn` (2 occurrences)

- **ImplementationDataTypeSubElementRef.implementation**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::PortInterface`
  - Kind: `attribute`, Multiplicity: `0..1`
- **AutosarVariableRef.autosarVariable**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior::DataElements`
  - Kind: `attribute`, Multiplicity: `0..1`

### `CompositeNetwork` (2 occurrences)

- **ReceiverComSpec.compositeNetwork**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Communication`
  - Kind: `attribute`, Multiplicity: `*`
- **SenderComSpec.compositeNetwork**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Communication`
  - Kind: `attribute`, Multiplicity: `*`

### `J1939Controller` (2 occurrences)

- **J1939ControllerApplicationToJ1939NmNodeMapping.j1939Controller**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SWmapping`
  - Kind: `reference`, Multiplicity: `0..1`
- **SystemMapping.j1939Controller**
  - Package: `M2::AUTOSARTemplates::SystemTemplate`
  - Kind: `attribute`, Multiplicity: `*`

### `LinOrderedConfigurable` (2 occurrences)

- **LinSlaveConfig.linOrdered**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Lin::LinTopology`
  - Kind: `attribute`, Multiplicity: `*`
- **LinCommunicationConnector.linOrdered**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Lin::LinTopology`
  - Kind: `attribute`, Multiplicity: `*`

### `BinaryManifest` (2 occurrences)

- **CpSoftwareClusterBinaryManifestDescriptor.resource**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SoftwareCluster::BinaryManifest`
  - Kind: `attribute`, Multiplicity: `*`
- **BinaryManifestResource.resource**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SoftwareCluster::BinaryManifest`
  - Kind: `reference`, Multiplicity: `0..1`

### `SwcExclusiveArea` (1 occurrences)

- **SwcInternalBehavior.exclusiveArea**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior`
  - Kind: `attribute`, Multiplicity: `*`

### `PlatformModule` (1 occurrences)

- **IdsPlatformInstantiation.network**
  - Package: `M2::AUTOSARTemplates::AdaptivePlatform::PlatformModuleDeployment::IntrusionDetectionSystem`
  - Kind: `reference`, Multiplicity: `*`

### `TimeBaseResource` (1 occurrences)

- **IdsPlatformInstantiation.timeBaseResource**
  - Package: `M2::AUTOSARTemplates::AdaptivePlatform::PlatformModuleDeployment::IntrusionDetectionSystem`
  - Kind: `reference`, Multiplicity: `0..1`

### `ModeInSwcBsw` (1 occurrences)

- **TimingModeInstance.modeInstance**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingCondition`
  - Kind: `attribute`, Multiplicity: `0..1`

### `CanClusterBusOff` (1 occurrences)

- **AbstractCanCluster.busOffRecovery**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Can::CanTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `CanControllerFd` (1 occurrences)

- **AbstractCanCommunicationControllerAttributes.canControllerFd**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Can::CanTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `CanControllerXl` (1 occurrences)

- **AbstractCanCommunicationControllerAttributes.canControllerXl**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Can::CanTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticUdsSeverity` (1 occurrences)

- **DiagnosticTroubleCodeUds.severity**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticTroubleCode`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticWwhObdDtc` (1 occurrences)

- **DiagnosticTroubleCodeUds.wwhObdDtc**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticTroubleCode`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticExtended` (1 occurrences)

- **DiagnosticTroubleCodeProps.extendedData**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticTroubleCode`
  - Kind: `reference`, Multiplicity: `*`

### `DiagnosticSignificance` (1 occurrences)

- **DiagnosticTroubleCodeProps.significance**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticTroubleCode`
  - Kind: `attribute`, Multiplicity: `0..1`

### `ModeSwitchEvent` (1 occurrences)

- **NvBlockDescriptor.modeSwitchEvent**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::NvBlockComponent`
  - Kind: `attribute`, Multiplicity: `*`

### `SupportBufferLocking` (1 occurrences)

- **CommunicationBufferLocking.supportBufferLocking**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior::PortAPIOptions`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DataLinkLayerRule` (1 occurrences)

- **FirewallRule.dataLinkLayerRule**
  - Package: `M2::AUTOSARTemplates::AdaptivePlatform::PlatformModuleDeployment::Firewall`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DdsRule` (1 occurrences)

- **FirewallRule.ddsRule**
  - Package: `M2::AUTOSARTemplates::AdaptivePlatform::PlatformModuleDeployment::Firewall`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DoIpRule` (1 occurrences)

- **FirewallRule.doIpRule**
  - Package: `M2::AUTOSARTemplates::AdaptivePlatform::PlatformModuleDeployment::Firewall`
  - Kind: `attribute`, Multiplicity: `0..1`

### `NetworkLayerRule` (1 occurrences)

- **FirewallRule.networkLayerRule**
  - Package: `M2::AUTOSARTemplates::AdaptivePlatform::PlatformModuleDeployment::Firewall`
  - Kind: `attribute`, Multiplicity: `0..1`

### `PayloadBytePattern` (1 occurrences)

- **FirewallRule.payloadBytePattern**
  - Package: `M2::AUTOSARTemplates::AdaptivePlatform::PlatformModuleDeployment::Firewall`
  - Kind: `attribute`, Multiplicity: `*`

### `SomeipProtocolRule` (1 occurrences)

- **FirewallRule.someipRule**
  - Package: `M2::AUTOSARTemplates::AdaptivePlatform::PlatformModuleDeployment::Firewall`
  - Kind: `attribute`, Multiplicity: `0..1`

### `SomeipSdRule` (1 occurrences)

- **FirewallRule.someipSdRule**
  - Package: `M2::AUTOSARTemplates::AdaptivePlatform::PlatformModuleDeployment::Firewall`
  - Kind: `attribute`, Multiplicity: `0..1`

### `TransportLayerRule` (1 occurrences)

- **FirewallRule.transportLayerRule**
  - Package: `M2::AUTOSARTemplates::AdaptivePlatform::PlatformModuleDeployment::Firewall`
  - Kind: `attribute`, Multiplicity: `0..1`

### `e.g` (1 occurrences)

- **J1939DcmIPdu.MessageType**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreCommunication`
  - Kind: `attribute`, Multiplicity: `1`

### `SecOcCryptoService` (1 occurrences)

- **PduTriggering.secOcCryptoService**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreCommunication`
  - Kind: `reference`, Multiplicity: `0..1`

### `TriggerIPduSend` (1 occurrences)

- **PduTriggering.triggerIPduSend**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreCommunication`
  - Kind: `attribute`, Multiplicity: `*`

### `IPduSignalProcessing` (1 occurrences)

- **IPduPort.iPduSignal**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreCommunication`
  - Kind: `attribute`, Multiplicity: `0..1`

### `ContainerIPduTrigger` (1 occurrences)

- **ContainerIPdu.containerTrigger**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreCommunication`
  - Kind: `attribute`, Multiplicity: `0..1`

### `ContainerIPduHeader` (1 occurrences)

- **ContainerIPdu.headerType**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreCommunication`
  - Kind: `attribute`, Multiplicity: `0..1`

### `RxAcceptContainedI` (1 occurrences)

- **ContainerIPdu.rxAccept**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreCommunication`
  - Kind: `attribute`, Multiplicity: `0..1`

### `ContainedIPdu` (1 occurrences)

- **ContainedIPduProps.collection**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreCommunication`
  - Kind: `attribute`, Multiplicity: `0..1`

### `SecuredPduHeader` (1 occurrences)

- **SecuredIPdu.useSecuredPdu**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreCommunication`
  - Kind: `attribute`, Multiplicity: `0..1`

### `SenderRecArray` (1 occurrences)

- **SenderRecArrayTypeMapping.arrayElement**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::DataMapping`
  - Kind: `attribute`, Multiplicity: `*`

### `SenderRecRecord` (1 occurrences)

- **SenderRecRecordTypeMapping.recordElement**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::DataMapping`
  - Kind: `attribute`, Multiplicity: `*`

### `ClassContent` (1 occurrences)

- **ClassTailoring.classContent**
  - Package: `M2::AUTOSARTemplates::CommonStructure::StandardizationTemplate::DataExchangePoint::Data`
  - Kind: `attribute`, Multiplicity: `*`

### `DefaultValueApplication` (1 occurrences)

- **PrimitiveAttributeTailoring.defaultValue**
  - Package: `M2::AUTOSARTemplates::CommonStructure::StandardizationTemplate::DataExchangePoint::Data`
  - Kind: `attribute`, Multiplicity: `0..1`

### `ValueRestrictionWith` (1 occurrences)

- **PrimitiveAttributeTailoring.valueRestrictionWithSeverity**
  - Package: `M2::AUTOSARTemplates::CommonStructure::StandardizationTemplate::DataExchangePoint::Data`
  - Kind: `attribute`, Multiplicity: `0..1`

### `UnresolvedReference` (1 occurrences)

- **ReferenceTailoring.unresolvedRestriction**
  - Package: `M2::AUTOSARTemplates::CommonStructure::StandardizationTemplate::DataExchangePoint::Data`
  - Kind: `attribute`, Multiplicity: `0..1`

### `SwServiceImplPolicy` (1 occurrences)

- **BswModuleEntry.swServiceImplPolicy**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswInterfaces`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticResponseTo` (1 occurrences)

- **DiagnosticEcuResetClass.respondTo**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::EcuReset`
  - Kind: `attribute`, Multiplicity: `0..1`

### `SwcBswSynchronized` (1 occurrences)

- **SwcBswMapping.synchronized**
  - Package: `M2::AUTOSARTemplates::CommonStructure::SwcBswMapping`
  - Kind: `attribute`, Multiplicity: `*`

### `EventOccurrenceKind` (1 occurrences)

- **SynchronizationTimingConstraint.event**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingConstraint::SynchronizationTiming`
  - Kind: `attribute`, Multiplicity: `0..1`

### `SynchronizationType` (1 occurrences)

- **SynchronizationTimingConstraint.synchronization**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingConstraint::SynchronizationTiming`
  - Kind: `attribute`, Multiplicity: `0..1`

### `BswPerInstance` (1 occurrences)

- **BswInternalBehavior.bswPerInstance**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `attribute`, Multiplicity: `*`

### `BswClientPolicy` (1 occurrences)

- **BswInternalBehavior.clientPolicy**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `attribute`, Multiplicity: `*`

### `BswExclusiveArea` (1 occurrences)

- **BswInternalBehavior.exclusiveArea**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `attribute`, Multiplicity: `*`

### `BswModeReceiver` (1 occurrences)

- **BswInternalBehavior.modeReceiver**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `attribute`, Multiplicity: `*`

### `BswParameterPolicy` (1 occurrences)

- **BswInternalBehavior.parameterPolicy**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `attribute`, Multiplicity: `*`

### `BswDataReception` (1 occurrences)

- **BswInternalBehavior.receptionPolicy**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `attribute`, Multiplicity: `*`

### `BswReleasedTrigger` (1 occurrences)

- **BswInternalBehavior.releasedTrigger**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `attribute`, Multiplicity: `*`

### `BswDataSendPolicy` (1 occurrences)

- **BswInternalBehavior.sendPolicy**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `attribute`, Multiplicity: `*`

### `BswTriggerDirect` (1 occurrences)

- **BswInternalBehavior.triggerDirect**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `attribute`, Multiplicity: `*`

### `BswModeSwitchAck` (1 occurrences)

- **BswModeSenderPolicy.ackRequestRequest**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `attribute`, Multiplicity: `0..1`

### `RoleBasedBswModule` (1 occurrences)

- **BswServiceDependency.assignedEntry**
  - Package: `M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior`
  - Kind: `attribute`, Multiplicity: `*`

### `DiagnosticRequestOn` (1 occurrences)

- **DiagnosticRequestOnBoardMonitoringTestResults.requestOn**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::ObdService::Mode_0x06_RequestOnBoard`
  - Kind: `reference`, Multiplicity: `0..1`

### `DiagnosticClear` (1 occurrences)

- **DiagnosticClearDiagnosticInformation.clearDiagnostic**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::ClearDiagnosticInfo`
  - Kind: `reference`, Multiplicity: `0..1`

### `DataTransformationKind` (1 occurrences)

- **DataTransformation.data**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Transformer`
  - Kind: `attribute`, Multiplicity: `0..1`

### `EndToEndProfile` (1 occurrences)

- **EndToEndTransformationDescription.profileBehaviorBehaviorEnum**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Transformer`
  - Kind: `attribute`, Multiplicity: `0..1`

### `CSTransformerError` (1 occurrences)

- **TransformationISignalProps.csErrorReaction**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Transformer`
  - Kind: `attribute`, Multiplicity: `0..1`

### `SOMEIPMessageType` (1 occurrences)

- **SOMEIPTransformationISignalProps.messageType**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Transformer`
  - Kind: `attribute`, Multiplicity: `0..1`

### `TimingClockSync` (1 occurrences)

- **TimingExtension.timingClockSync**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingExtensions`
  - Kind: `attribute`, Multiplicity: `*`

### `ExecutionOrder` (1 occurrences)

- **ExecutionOrderConstraint.executionOrder**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingConstraint::ExecutionOrderConstraint`
  - Kind: `attribute`, Multiplicity: `0..1`

### `LetDataExchange` (1 occurrences)

- **EOCExecutableEntityRefGroup.letDataExchange**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingConstraint::ExecutionOrderConstraint`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticOccurrence` (1 occurrences)

- **DiagnosticCommonProps.occurrence**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticCommonProps`
  - Kind: `attribute`, Multiplicity: `0..1`

### `EthernetConnection` (1 occurrences)

- **CouplingPort.connection**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `EthernetPhysicalLayer` (1 occurrences)

- **CouplingPort.physicalLayer**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DhcpServer` (1 occurrences)

- **VlanMembership.dhcpAddress**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `EthernetPriority` (1 occurrences)

- **CouplingPortDetails.ethernetPriority**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `1`

### `CouplingPortTraffic` (1 occurrences)

- **CouplingPortDetails.ethernetTraffic**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `1`

### `GlobalTimeCoupling` (1 occurrences)

- **CouplingPortDetails.globalTimeCoupling**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `EthernetCouplingPort` (1 occurrences)

- **CouplingPortScheduler.portSchedulerSchedulerEnum**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `CouplingPortAbstract` (1 occurrences)

- **CouplingPortFifo.shaper**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `Ipv4DhcpServer` (1 occurrences)

- **DhcpServerConfiguration.ipv4DhcpServer**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `Ipv6DhcpServer` (1 occurrences)

- **DhcpServerConfiguration.ipv6DhcpServer**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `SwitchStream` (1 occurrences)

- **CouplingElementSwitchDetails.switchStream**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `*`

### `StreamFilterRuleData` (1 occurrences)

- **SwitchStreamFilterRule.dataLinkLayer**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `StreamFilterIEEE1722` (1 occurrences)

- **SwitchStreamFilterRule.ieee1722Tp**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `FlowMeteringColor` (1 occurrences)

- **SwitchFlowMeteringEntry.colorMode**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `Ipv4Fragmentation` (1 occurrences)

- **Ipv4Props.fragmentation**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `Ipv6Fragmentation` (1 occurrences)

- **Ipv6Props.fragmentation**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `BooleanRecovery` (1 occurrences)

- **TcpProps.tcpFastRecovery**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `TlsCryptoService` (1 occurrences)

- **ApplicationEndpoint.tlsCryptoService**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `reference`, Multiplicity: `0..1`

### `TransportProtocol` (1 occurrences)

- **ApplicationEndpoint.tpConfigurationConfiguration**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `RequestMethodEnum` (1 occurrences)

- **HttpTp.requestMethodEnum**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `Ipv4AddressSource` (1 occurrences)

- **Ipv4Configuration.ipv4AddressSource**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `Ipv6AddressSource` (1 occurrences)

- **Ipv6Configuration.ipv6AddressSource**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `TimeSyncClient` (1 occurrences)

- **TimeSynchronization.timeSyncClientConfiguration**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::EthernetTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticEnvCondition` (1 occurrences)

- **DiagnosticEnvironmentalCondition.formula**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::EnvironmentalCondition`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticLogical` (1 occurrences)

- **DiagnosticEnvConditionFormula.op**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::EnvironmentalCondition`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticCompare` (1 occurrences)

- **DiagnosticEnvCompareCondition.compareType**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::EnvironmentalCondition`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticMemoryEntry` (1 occurrences)

- **DiagnosticMemoryDestination.memoryEntry**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticMemoryDestination`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticTypeOf` (1 occurrences)

- **DiagnosticMemoryDestination.typeOfFreeze**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticMemoryDestination`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticTypeOfDtc` (1 occurrences)

- **DiagnosticMemoryDestinationPrimary.typeOfDtc**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticMemoryDestination`
  - Kind: `attribute`, Multiplicity: `0..1`

### `TDCpSoftwareCluster` (1 occurrences)

- **TDCpSoftwareClusterMappingSet.tdCpSoftware**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingCpSoftwareCluster`
  - Kind: `attribute`, Multiplicity: `*`

### `RoleBasedResource` (1 occurrences)

- **CpSoftwareClusterResource.dependent**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SoftwareCluster`
  - Kind: `attribute`, Multiplicity: `*`

### `DataConsistencyPolicy` (1 occurrences)

- **DataComProps.data**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SoftwareCluster`
  - Kind: `attribute`, Multiplicity: `0..1`

### `SomeipSdClientEvent` (1 occurrences)

- **ConsumedEventGroup.sdClientTimer**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ServiceInstances`
  - Kind: `reference`, Multiplicity: `0..1`

### `SomeipSdClientService` (1 occurrences)

- **ConsumedServiceInstance.sdClientTimer**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ServiceInstances`
  - Kind: `reference`, Multiplicity: `0..1`

### `ServiceVersion` (1 occurrences)

- **ConsumedServiceInstance.versionDriven**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ServiceInstances`
  - Kind: `attribute`, Multiplicity: `0..1`

### `SomeipSdServer` (1 occurrences)

- **ProvidedServiceInstance.sdServerTimer**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ServiceInstances`
  - Kind: `reference`, Multiplicity: `0..1`

### `UdpChecksum` (1 occurrences)

- **SocketAddress.udpChecksum**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ServiceInstances`
  - Kind: `attribute`, Multiplicity: `0..1`

### `AbstractService` (1 occurrences)

- **ServiceInstanceCollectionSet.serviceInstance**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ServiceInstances`
  - Kind: `attribute`, Multiplicity: `*`

### `PduCollection` (1 occurrences)

- **SoConIPduIdentifier.pduCollection**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ServiceInstances`
  - Kind: `attribute`, Multiplicity: `0..1`

### `SomeipSdServerEvent` (1 occurrences)

- **EventHandler.sdServerEg**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ServiceInstances`
  - Kind: `reference`, Multiplicity: `0..1`

### `ModeDriven` (1 occurrences)

- **TransmissionModeDeclaration.modeDriven**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreCommunication::Timing`
  - Kind: `attribute`, Multiplicity: `*`

### `DiagnosticObdSupport` (1 occurrences)

- **DiagnosticEcuInstanceProps.obdSupport**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::DiagnosticContribution`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticWriteMemory` (1 occurrences)

- **DiagnosticWriteMemoryByAddress.writeClass**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::MemoryByAddress`
  - Kind: `reference`, Multiplicity: `0..1`

### `DiagnosticReadMemory` (1 occurrences)

- **DiagnosticReadMemoryByAddress.readClass**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::MemoryByAddress`
  - Kind: `reference`, Multiplicity: `0..1`

### `DiagnosticAbstractData` (1 occurrences)

- **DiagnosticDataByIdentifier.dataIdentifier**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::DataByIdentifier`
  - Kind: `reference`, Multiplicity: `0..1`

### `DiagnosticReadScaling` (1 occurrences)

- **DiagnosticReadScalingDataByIdentifier.readScaling**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::DataByIdentifier`
  - Kind: `reference`, Multiplicity: `0..1`

### `CompositeValue` (1 occurrences)

- **CompositeRuleBasedValueSpecification.argument**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Constants`
  - Kind: `attribute`, Multiplicity: `*`

### `CompositeRuleBased` (1 occurrences)

- **CompositeRuleBasedValueSpecification.compound**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Constants`
  - Kind: `attribute`, Multiplicity: `*`

### `ModeErrorReaction` (1 occurrences)

- **ModeErrorBehavior.errorReaction**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ModeDeclaration`
  - Kind: `attribute`, Multiplicity: `0..1`

### `CryptoObjectTypeEnum` (1 occurrences)

- **CryptoKeySlot.cryptoObjectTypeEnum**
  - Package: `M2::AUTOSARTemplates::AdaptivePlatform::PlatformModuleDeployment::CryptoDeployment`
  - Kind: `attribute`, Multiplicity: `0..1`

### `CryptoKeySlotAllowed` (1 occurrences)

- **CryptoKeySlot.keySlotAllowed**
  - Package: `M2::AUTOSARTemplates::AdaptivePlatform::PlatformModuleDeployment::CryptoDeployment`
  - Kind: `attribute`, Multiplicity: `0..1`

### `CryptoKeySlotContent` (1 occurrences)

- **CryptoKeySlot.keySlotContent**
  - Package: `M2::AUTOSARTemplates::AdaptivePlatform::PlatformModuleDeployment::CryptoDeployment`
  - Kind: `attribute`, Multiplicity: `*`

### `CryptoKeySlotType` (1 occurrences)

- **CryptoKeySlot.slotType**
  - Package: `M2::AUTOSARTemplates::AdaptivePlatform::PlatformModuleDeployment::CryptoDeployment`
  - Kind: `attribute`, Multiplicity: `0..1`

### `RoleBasedDataType` (1 occurrences)

- **ServiceDependency.assignedData**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ServiceNeeds`
  - Kind: `attribute`, Multiplicity: `0..1`

### `ServiceDiagnostic` (1 occurrences)

- **ServiceDependency.diagnostic**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ServiceNeeds`
  - Kind: `attribute`, Multiplicity: `0..1`

### `RamBlockStatusControl` (1 occurrences)

- **NvBlockNeeds.ramBlockStatusControl**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ServiceNeeds`
  - Kind: `attribute`, Multiplicity: `0..1`

### `NvBlockNeedsWriting` (1 occurrences)

- **NvBlockNeeds.writingPriority**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ServiceNeeds`
  - Kind: `attribute`, Multiplicity: `0..1`

### `SupervisedEntity` (1 occurrences)

- **SupervisedEntityNeeds.checkpoints**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ServiceNeeds`
  - Kind: `reference`, Multiplicity: `*`

### `DiagnosticAudience` (1 occurrences)

- **DiagnosticCapabilityElement.audience**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ServiceNeeds`
  - Kind: `attribute`, Multiplicity: `*`

### `DiagRequirementId` (1 occurrences)

- **DiagnosticCapabilityElement.diag**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ServiceNeeds`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticValueAccess` (1 occurrences)

- **DiagnosticValueNeeds.diagnosticValueAccess**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ServiceNeeds`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticProcessing` (1 occurrences)

- **DiagnosticValueNeeds.processingStyle**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ServiceNeeds`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticRoutineType` (1 occurrences)

- **DiagnosticRoutineNeeds.diagRoutine**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ServiceNeeds`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagEventDebounce` (1 occurrences)

- **DiagnosticEventNeeds.diagEventDebounce**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ServiceNeeds`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticMonitor` (1 occurrences)

- **ObdMonitorServiceNeeds.updateKind**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ServiceNeeds`
  - Kind: `attribute`, Multiplicity: `0..1`

### `OperationCycleType` (1 occurrences)

- **DiagnosticOperationCycleNeeds.operationCycle**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ServiceNeeds`
  - Kind: `attribute`, Multiplicity: `0..1`

### `EventAcceptanceStatus` (1 occurrences)

- **DiagnosticEnableConditionNeeds.initialStatus**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ServiceNeeds`
  - Kind: `attribute`, Multiplicity: `0..1`

### `StorageConditionStatus` (1 occurrences)

- **DiagnosticStorageConditionNeeds.initialStatus**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ServiceNeeds`
  - Kind: `attribute`, Multiplicity: `0..1`

### `ObdRatioConnection` (1 occurrences)

- **ObdRatioServiceNeeds.connectionType**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ServiceNeeds`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticDenominator` (1 occurrences)

- **ObdRatioDenominatorNeeds.denominator**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ServiceNeeds`
  - Kind: `attribute`, Multiplicity: `0..1`

### `VerificationStatus` (1 occurrences)

- **SecureOnBoardCommunicationNeeds.verification**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ServiceNeeds`
  - Kind: `attribute`, Multiplicity: `0..1`

### `PossibleErrorReaction` (1 occurrences)

- **TransientFault.possibleErrorReaction**
  - Package: `M2::AUTOSARTemplates::CommonStructure::ServiceNeeds`
  - Kind: `attribute`, Multiplicity: `*`

### `FlexrayAbsolutely` (1 occurrences)

- **FlexrayFrameTriggering.absolutely**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Flexray::FlexrayCommunication`
  - Kind: `attribute`, Multiplicity: `*`

### `BooleanIndicator` (1 occurrences)

- **FlexrayFrameTriggering.payloadPreamble**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Flexray::FlexrayCommunication`
  - Kind: `attribute`, Multiplicity: `0..1`

### `TtcanAbsolutely` (1 occurrences)

- **CanFrameTriggering.absolutely**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Can::CanCommunication`
  - Kind: `attribute`, Multiplicity: `*`

### `CanFrameRxBehavior` (1 occurrences)

- **CanFrameTriggering.canFrameRxBehavior**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Can::CanCommunication`
  - Kind: `attribute`, Multiplicity: `0..1`

### `CanXlFrameTriggering` (1 occurrences)

- **CanFrameTriggering.canXlFrame**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Can::CanCommunication`
  - Kind: `attribute`, Multiplicity: `0..1`

### `InstantiationRTEEvent` (1 occurrences)

- **CompositionSwComponentType.instantiationRTEEvent**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Composition`
  - Kind: `attribute`, Multiplicity: `*`

### `SwCalprmAxisType` (1 occurrences)

- **SwCalprmAxis.swCalprmAxis**
  - Package: `M2::MSR::DataDictionary::CalibrationParameter`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DdsOwnershipKind` (1 occurrences)

- **DdsOwnership.ownershipKind**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::Dds`
  - Kind: `attribute`, Multiplicity: `0..1`

### `SocketConnectionIpdu` (1 occurrences)

- **SocketConnection.pdu**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Ethernet::ObsoleteModel`
  - Kind: `attribute`, Multiplicity: `*`

### `DisplayPresentation` (1 occurrences)

- **SwDataDefProps.display**
  - Package: `M2::MSR::DataDictionary::DataDefProperties`
  - Kind: `attribute`, Multiplicity: `0..1`

### `AsamRecordLayout` (1 occurrences)

- **SwRecordLayoutGroup.category**
  - Package: `M2::MSR::DataDictionary::RecordLayout`
  - Kind: `attribute`, Multiplicity: `0..1`

### `RecordLayoutIterator` (1 occurrences)

- **SwRecordLayoutGroup.swRecord**
  - Package: `M2::MSR::DataDictionary::RecordLayout`
  - Kind: `attribute`, Multiplicity: `0..1`

### `EthGlobalTime` (1 occurrences)

- **EthGlobalTimeDomainProps.managed**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::GlobalTime::ETH`
  - Kind: `attribute`, Multiplicity: `*`

### `EthGlobalTimeMessage` (1 occurrences)

- **EthGlobalTimeDomainProps.message**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::GlobalTime::ETH`
  - Kind: `attribute`, Multiplicity: `0..1`

### `GlobalTimePortRole` (1 occurrences)

- **EthGlobalTimeManagedCouplingPort.globalTimePortRole**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::GlobalTime::ETH`
  - Kind: `attribute`, Multiplicity: `0..1`

### `TDEventVariableData` (1 occurrences)

- **TDEventVariableDataPrototype.tdEventVariableType**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingDescription::TimingDescription`
  - Kind: `attribute`, Multiplicity: `0..1`

### `TDEventOperationType` (1 occurrences)

- **TDEventOperation.tdEvent**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingDescription::TimingDescription`
  - Kind: `attribute`, Multiplicity: `0..1`

### `TDEventMode` (1 occurrences)

- **TDEventModeDeclaration.tdEventMode**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingDescription::TimingDescription`
  - Kind: `attribute`, Multiplicity: `0..1`

### `TDEventTriggerType` (1 occurrences)

- **TDEventTrigger.tdEventTrigger**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingDescription::TimingDescription`
  - Kind: `attribute`, Multiplicity: `0..1`

### `TDEventSwcInternal` (1 occurrences)

- **TDEventSwcInternalBehavior.tdEventSwcBehaviorType**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingDescription::TimingDescription`
  - Kind: `attribute`, Multiplicity: `0..1`

### `TDEventISignalType` (1 occurrences)

- **TDEventISignal.tdEventTypeEnum**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingDescription::TimingDescription`
  - Kind: `attribute`, Multiplicity: `0..1`

### `TDEventFrameType` (1 occurrences)

- **TDEventFrame.tdEventTypeEnum**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingDescription::TimingDescription`
  - Kind: `attribute`, Multiplicity: `0..1`

### `TDEventBswInternal` (1 occurrences)

- **TDEventBswInternalBehavior.tdEventBswBehaviorType**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingDescription::TimingDescription`
  - Kind: `attribute`, Multiplicity: `0..1`

### `TDEventBswMode` (1 occurrences)

- **TDEventBswModeDeclaration.tdEventBswDeclarationType**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingDescription::TimingDescription`
  - Kind: `attribute`, Multiplicity: `0..1`

### `CompuNominator` (1 occurrences)

- **CompuRationalCoeffs.compu**
  - Package: `M2::MSR::AsamHdo::ComputationMethod`
  - Kind: `attribute`, Multiplicity: `0..1`

### `ShowResourceAlias` (1 occurrences)

- **Xref.showResourceAlias**
  - Package: `M2::MSR::Documentation::TextModel::InlineTextElements`
  - Kind: `attribute`, Multiplicity: `0..1`

### `ShowResourceType` (1 occurrences)

- **Xref.showResource**
  - Package: `M2::MSR::Documentation::TextModel::InlineTextElements`
  - Kind: `attribute`, Multiplicity: `0..1`

### `ShowResourceLong` (1 occurrences)

- **Xref.showResourceLong**
  - Package: `M2::MSR::Documentation::TextModel::InlineTextElements`
  - Kind: `attribute`, Multiplicity: `0..1`

### `ShowResourceNumber` (1 occurrences)

- **Xref.showResourceNumber**
  - Package: `M2::MSR::Documentation::TextModel::InlineTextElements`
  - Kind: `attribute`, Multiplicity: `0..1`

### `ShowResourcePage` (1 occurrences)

- **Xref.showResourcePage**
  - Package: `M2::MSR::Documentation::TextModel::InlineTextElements`
  - Kind: `attribute`, Multiplicity: `0..1`

### `ShowResourceShort` (1 occurrences)

- **Xref.showResourceShort**
  - Package: `M2::MSR::Documentation::TextModel::InlineTextElements`
  - Kind: `attribute`, Multiplicity: `0..1`

### `TraceableTable` (1 occurrences)

- **TopicContent.traceableTable**
  - Package: `M2::MSR::Documentation::Chapters`
  - Kind: `attribute`, Multiplicity: `1`

### `DiagnosticClearEvent` (1 occurrences)

- **DiagnosticEvent.clearEvent**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticEvent`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticEventClear` (1 occurrences)

- **DiagnosticEvent.eventClear**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticEvent`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticEventKind` (1 occurrences)

- **DiagnosticEvent.eventKind**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticEvent`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticIumprKind` (1 occurrences)

- **DiagnosticIumpr.ratioKind**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticEvent`
  - Kind: `attribute`, Multiplicity: `0..1`

### `LifeCycleStateDefinition` (1 occurrences)

- **LifeCycleInfoSet.usedLifeCycle**
  - Package: `M2::AUTOSARTemplates::GenericStructure::LifeCycles`
  - Kind: `reference`, Multiplicity: `1`

### `AbstractDoIpLogic` (1 occurrences)

- **DoIpLogicAddress.doIpLogic**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::TransportProtocols`
  - Kind: `attribute`, Multiplicity: `0..1`

### `TpAckType` (1 occurrences)

- **FlexrayTpConnectionControl.ackType**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::TransportProtocols`
  - Kind: `attribute`, Multiplicity: `0..1`

### `MaximumMessage` (1 occurrences)

- **FlexrayArTpChannel.maximumMessage**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::TransportProtocols`
  - Kind: `attribute`, Multiplicity: `0..1`

### `FlexrayCommunication` (1 occurrences)

- **FlexrayArTpNode.connector**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::TransportProtocols`
  - Kind: `reference`, Multiplicity: `*`

### `CanTpAddressing` (1 occurrences)

- **CanTpConnection.addressing**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::TransportProtocols`
  - Kind: `attribute`, Multiplicity: `0..1`

### `NetworkTargetAddress` (1 occurrences)

- **CanTpConnection.taTypeType**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::TransportProtocols`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticCustom` (1 occurrences)

- **DiagnosticCustomServiceInstance.customService**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::CustomServiceInstance`
  - Kind: `reference`, Multiplicity: `0..1`

### `DiagnosticReadDTC` (1 occurrences)

- **DiagnosticReadDTCInformation.read**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::ReadDTCInformation`
  - Kind: `reference`, Multiplicity: `0..1`

### `ScaleConstrValidity` (1 occurrences)

- **ScaleConstr.validity**
  - Package: `M2::MSR::AsamHdo::Constraints::GlobalConstraints`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticControl` (1 occurrences)

- **DiagnosticIOControl.controlEnable**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::IOControl`
  - Kind: `attribute`, Multiplicity: `*`

### `DiagnosticIoControl` (1 occurrences)

- **DiagnosticIOControl.ioControlClass**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::IOControl`
  - Kind: `reference`, Multiplicity: `0..1`

### `DiagnosticDynamicData` (1 occurrences)

- **DiagnosticDynamicallyDefineDataIdentifier.dataIdentifier**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::DynamicallyDefineDataIdentifier`
  - Kind: `reference`, Multiplicity: `0..1`

### `DiagnosticHandleDDDI` (1 occurrences)

- **DiagnosticDynamicallyDefineDataIdentifierClass.configuration**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::DynamicallyDefineDataIdentifier`
  - Kind: `attribute`, Multiplicity: `0..1`

### `IEEE1722TpCrfPull` (1 occurrences)

- **IEEE1722TpCrfConnection.crfPullEnum**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::TransportProtocols::IEEE1722Tp::IEEE1722TpAv`
  - Kind: `attribute`, Multiplicity: `0..1`

### `IEEE1722TpCrfType` (1 occurrences)

- **IEEE1722TpCrfConnection.crfTypeEnum**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::TransportProtocols::IEEE1722Tp::IEEE1722TpAv`
  - Kind: `attribute`, Multiplicity: `0..1`

### `IEEE1722TpAafAes3` (1 occurrences)

- **IEEE1722TpAafConnection.aafAes3Data**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::TransportProtocols::IEEE1722Tp::IEEE1722TpAv`
  - Kind: `attribute`, Multiplicity: `0..1`

### `IEEE1722TpAafFormat` (1 occurrences)

- **IEEE1722TpAafConnection.aafFormatEnum**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::TransportProtocols::IEEE1722Tp::IEEE1722TpAv`
  - Kind: `attribute`, Multiplicity: `0..1`

### `IEEE1722TpAaf` (1 occurrences)

- **IEEE1722TpAafConnection.aafNominalRate**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::TransportProtocols::IEEE1722Tp::IEEE1722TpAv`
  - Kind: `attribute`, Multiplicity: `0..1`

### `IEEE1722TpRvfColor` (1 occurrences)

- **IEEE1722TpRvfConnection.rvfColorSpace**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::TransportProtocols::IEEE1722Tp::IEEE1722TpAv`
  - Kind: `attribute`, Multiplicity: `0..1`

### `IEEE1722TpRvfFrame` (1 occurrences)

- **IEEE1722TpRvfConnection.rvfFrameRate**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::TransportProtocols::IEEE1722Tp::IEEE1722TpAv`
  - Kind: `attribute`, Multiplicity: `0..1`

### `BaseTypeEncoding` (1 occurrences)

- **BaseTypeDirectDefinition.baseTypeEncoding**
  - Package: `M2::MSR::AsamHdo::BaseTypes`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DelegatedPort` (1 occurrences)

- **PortPrototype.delegatedPort**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Components`
  - Kind: `attribute`, Multiplicity: `0..1`

### `IoHwAbstractionServer` (1 occurrences)

- **PortPrototype.ioHwAbstractionServerAnnotation**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Components`
  - Kind: `attribute`, Multiplicity: `*`

### `ParameterPort` (1 occurrences)

- **PortPrototype.parameterPort**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Components`
  - Kind: `attribute`, Multiplicity: `*`

### `SwComponentMapping` (1 occurrences)

- **SwComponentType.swcMapping**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Components`
  - Kind: `reference`, Multiplicity: `*`

### `DiagnosticPowertrain` (1 occurrences)

- **DiagnosticRequestPowertrainFreezeFrameData.freezeFrameFreezeFrame**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::ObdService::Mode_0x02_RequestPowertrainFreeze`
  - Kind: `reference`, Multiplicity: `0..1`

### `RptExecutionControl` (1 occurrences)

- **RptExecutableEntityProperties.rptExecutionControl**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::RPTScenario`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticTestRoutine` (1 occurrences)

- **DiagnosticRequestControlOfOnBoardDevice.testIdIdentifier**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::ObdService::Mode_0x08_RequestControlOfOnBoard`
  - Kind: `reference`, Multiplicity: `0..1`

### `OsTaskPreemptability` (1 occurrences)

- **OsTaskProxy.preemptability**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::RteEventToOsTaskMapping`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticJumpToBoot` (1 occurrences)

- **DiagnosticSession.jumpToBoot**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm`
  - Kind: `attribute`, Multiplicity: `0..1`

### `SpecificationDocument` (1 occurrences)

- **SpecificationScope.specificationDocument**
  - Package: `M2::AUTOSARTemplates::CommonStructure::StandardizationTemplate::DataExchange`
  - Kind: `attribute`, Multiplicity: `*`

### `DocumentElement` (1 occurrences)

- **SpecificationDocumentScope.document**
  - Package: `M2::AUTOSARTemplates::CommonStructure::StandardizationTemplate::DataExchange`
  - Kind: `attribute`, Multiplicity: `*`

### `TraceableElement` (1 occurrences)

- **DocumentElementScope.customDocument**
  - Package: `M2::AUTOSARTemplates::CommonStructure::StandardizationTemplate::DataExchange`
  - Kind: `reference`, Multiplicity: `0..1`

### `DataFormatElement` (1 occurrences)

- **DocumentElementScope.tailoring**
  - Package: `M2::AUTOSARTemplates::CommonStructure::StandardizationTemplate::DataExchange`
  - Kind: `reference`, Multiplicity: `*`

### `EcucParamConf` (1 occurrences)

- **EcucChoiceContainerDef.choice**
  - Package: `M2::AUTOSARTemplates::ECUCParameterDefTemplate`
  - Kind: `attribute`, Multiplicity: `*`

### `EcucValidation` (1 occurrences)

- **EcucDefinitionElement.ecucValidation**
  - Package: `M2::AUTOSARTemplates::ECUCParameterDefTemplate`
  - Kind: `attribute`, Multiplicity: `*`

### `EcucValueConfiguration` (1 occurrences)

- **EcucCommonAttributes.valueConfig**
  - Package: `M2::AUTOSARTemplates::ECUCParameterDefTemplate`
  - Kind: `attribute`, Multiplicity: `*`

### `EcucConfigurationClass` (1 occurrences)

- **EcucAbstractConfigurationClass.configClass**
  - Package: `M2::AUTOSARTemplates::ECUCParameterDefTemplate`
  - Kind: `attribute`, Multiplicity: `0..1`

### `EcucDerivation` (1 occurrences)

- **EcucParameterDef.derivation**
  - Package: `M2::AUTOSARTemplates::ECUCParameterDefTemplate`
  - Kind: `attribute`, Multiplicity: `0..1`

### `EcucEnumerationLiteral` (1 occurrences)

- **EcucEnumerationParamDef.literal**
  - Package: `M2::AUTOSARTemplates::ECUCParameterDefTemplate`
  - Kind: `attribute`, Multiplicity: `*`

### `EcucParameter` (1 occurrences)

- **EcucDerivationSpecification.calculation**
  - Package: `M2::AUTOSARTemplates::ECUCParameterDefTemplate`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticInhibition` (1 occurrences)

- **DiagnosticFunctionIdentifierInhibit.inhibitionMask**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Fim`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DltDefaultTraceState` (1 occurrences)

- **DltLogChannel.defaultTrace**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Dlt`
  - Kind: `attribute`, Multiplicity: `0..1`

### `LogTraceDefaultLog` (1 occurrences)

- **DltLogChannel.logTraceDefaultLog**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Dlt`
  - Kind: `attribute`, Multiplicity: `0..1`

### `ServerArgumentImpl` (1 occurrences)

- **ArgumentDataPrototype.serverArgumentImpl**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::PortInterface`
  - Kind: `attribute`, Multiplicity: `0..1`

### `ClientServerApplication` (1 occurrences)

- **ClientServerInterfaceMapping.errorMapping**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::PortInterface`
  - Kind: `attribute`, Multiplicity: `*`

### `ArParameterIn` (1 occurrences)

- **ImplementationDataTypeSubElementRef.parameter**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::PortInterface`
  - Kind: `attribute`, Multiplicity: `0..1`

### `Transmission` (1 occurrences)

- **SenderComSpec.transmission**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Communication`
  - Kind: `attribute`, Multiplicity: `0..1`

### `TransmissionComSpec` (1 occurrences)

- **SenderComSpec.transmissionComSpec**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Communication`
  - Kind: `attribute`, Multiplicity: `0..1`

### `SwDataDefPropsRepresentation` (1 occurrences)

- **CompositeNetworkRepresentation.networkRepresentation**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Communication`
  - Kind: `attribute`, Multiplicity: `0..1`

### `ModeSwitchedAck` (1 occurrences)

- **ModeSwitchSenderComSpec.modeSwitchedAck**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::Communication`
  - Kind: `attribute`, Multiplicity: `0..1`

### `Programminglanguage` (1 occurrences)

- **Implementation.programming**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Implementation`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DependencyUsage` (1 occurrences)

- **DependencyOnArtifact.usage**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Implementation`
  - Kind: `attribute`, Multiplicity: `*`

### `McSwEmulationMethod` (1 occurrences)

- **McSupportData.emulation**
  - Package: `M2::AUTOSARTemplates::CommonStructure::MeasurementCalibrationSupport`
  - Kind: `attribute`, Multiplicity: `*`

### `ImplementationElement` (1 occurrences)

- **McDataInstance.instanceIn**
  - Package: `M2::AUTOSARTemplates::CommonStructure::MeasurementCalibrationSupport`
  - Kind: `attribute`, Multiplicity: `0..1`

### `McParameterElement` (1 occurrences)

- **McSwEmulationMethodSupport.elementGroup**
  - Package: `M2::AUTOSARTemplates::CommonStructure::MeasurementCalibrationSupport`
  - Kind: `attribute`, Multiplicity: `*`

### `MultiLanguage` (1 occurrences)

- **DocumentationBlock.p**
  - Package: `M2::MSR::Documentation::BlockElements`
  - Kind: `attribute`, Multiplicity: `0..1`

### `BusMirrorCanIdRange` (1 occurrences)

- **BusMirrorChannelMappingCan.canIdRange**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::BusMirror`
  - Kind: `attribute`, Multiplicity: `*`

### `BusMirrorCanIdToCanId` (1 occurrences)

- **BusMirrorChannelMappingCan.canIdToCanId**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::BusMirror`
  - Kind: `attribute`, Multiplicity: `*`

### `BusMirrorLinPidToCan` (1 occurrences)

- **BusMirrorChannelMappingCan.linPidToCanId**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::BusMirror`
  - Kind: `attribute`, Multiplicity: `*`

### `DoIpLogicTarget` (1 occurrences)

- **DoIpRoutingActivation.doIpTarget**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::DoIP`
  - Kind: `reference`, Multiplicity: `*`

### `J1939NmAddress` (1 occurrences)

- **J1939NmNode.address**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::NetworkManagement`
  - Kind: `attribute`, Multiplicity: `0..1`

### `NmCoordinatorRole` (1 occurrences)

- **NmNode.nmCoordinatorRole**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::NetworkManagement`
  - Kind: `attribute`, Multiplicity: `0..1`

### `FlexrayNmSchedule` (1 occurrences)

- **FlexrayNmClusterCoupling.nmSchedule**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::NetworkManagement`
  - Kind: `attribute`, Multiplicity: `0..1`

### `BooleanCapable` (1 occurrences)

- **J1939NodeName.arbitraryAddress**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::NetworkManagement`
  - Kind: `attribute`, Multiplicity: `0..1`

### `VariableAccessScope` (1 occurrences)

- **VariableAccess.scope**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior::DataElements`
  - Kind: `attribute`, Multiplicity: `0..1`

### `PduMappingDefault` (1 occurrences)

- **TargetIPduRef.defaultValue**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Multiplatform`
  - Kind: `attribute`, Multiplicity: `0..1`

### `RteApiReturnValue` (1 occurrences)

- **AbstractAccessPoint.returnValue**
  - Package: `M2::AUTOSARTemplates::SWComponentTemplate::SwcInternalBehavior::AccessCount`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticControlDTC` (1 occurrences)

- **DiagnosticControlDTCSetting.dtcSettingClass**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::ControlDTCSetting`
  - Kind: `reference`, Multiplicity: `0..1`

### `LatencyConstraintType` (1 occurrences)

- **LatencyTimingConstraint.latency**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingConstraint::LatencyTimingConstraint`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticSecurity` (1 occurrences)

- **DiagnosticSecurityAccess.securityAccess**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::SecurityAccess`
  - Kind: `reference`, Multiplicity: `0..1`

### `AbstractGlobalTime` (1 occurrences)

- **GlobalTimeDomain.globalTime**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::GlobalTime`
  - Kind: `attribute`, Multiplicity: `0..1`

### `NetworkSegment` (1 occurrences)

- **GlobalTimeDomain.network**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::GlobalTime`
  - Kind: `attribute`, Multiplicity: `0..1`

### `GlobalTimeIcvSupport` (1 occurrences)

- **GlobalTimeMaster.icvSecured**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::GlobalTime`
  - Kind: `attribute`, Multiplicity: `0..1`

### `GlobalTimeIcv` (1 occurrences)

- **GlobalTimeSlave.icvVerification**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::GlobalTime`
  - Kind: `attribute`, Multiplicity: `0..1`

### `V2xSupportEnum` (1 occurrences)

- **EcuInstance.v2xSupported**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::FibexCore::CoreTopology`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticClearReset` (1 occurrences)

- **DiagnosticClearResetEmissionRelatedInfo.clearReset**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::ObdService::Mode_0x04_ClearResetEmission`
  - Kind: `reference`, Multiplicity: `0..1`

### `CryptoCertificate` (1 occurrences)

- **CryptoServiceCertificate.algorithmFamily**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SecureCommunication`
  - Kind: `attribute`, Multiplicity: `0..1`

### `CryptoCertificateFormat` (1 occurrences)

- **CryptoServiceCertificate.format**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SecureCommunication`
  - Kind: `attribute`, Multiplicity: `0..1`

### `MacSecGlobalKay` (1 occurrences)

- **MacSecLocalKayProps.globalKayProps**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SecureCommunication`
  - Kind: `reference`, Multiplicity: `0..1`

### `MacSecCryptoAlgo` (1 occurrences)

- **MacSecKayParticipant.cryptoAlgo**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SecureCommunication`
  - Kind: `attribute`, Multiplicity: `0..1`

### `MacSecCipherSuite` (1 occurrences)

- **MacSecCryptoAlgoConfig.cipherSuite**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SecureCommunication`
  - Kind: `attribute`, Multiplicity: `1`

### `MacSecConfidentiality` (1 occurrences)

- **MacSecCryptoAlgoConfig.confidentiality**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SecureCommunication`
  - Kind: `attribute`, Multiplicity: `0..1`

### `CryptoEllipticCurve` (1 occurrences)

- **TlsCryptoCipherSuite.ellipticCurve**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SecureCommunication`
  - Kind: `reference`, Multiplicity: `*`

### `CryptoSignature` (1 occurrences)

- **TlsCryptoCipherSuite.signature**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SecureCommunication`
  - Kind: `reference`, Multiplicity: `*`

### `GeneralParameter` (1 occurrences)

- **Prms.prm**
  - Package: `M2::MSR::Documentation::BlockElements::GerneralParameters`
  - Kind: `attribute`, Multiplicity: `1`

### `ExecutionTimeType` (1 occurrences)

- **ExecutionTimeConstraint.executionTime**
  - Package: `M2::AUTOSARTemplates::CommonStructure::Timing::TimingConstraint::ExecutionTimeConstraint`
  - Kind: `attribute`, Multiplicity: `0..1`

### `ByteOrderEnumOrder` (1 occurrences)

- **System.containerIPduHeaderByte**
  - Package: `M2::AUTOSARTemplates::SystemTemplate`
  - Kind: `attribute`, Multiplicity: `0..1`

### `J1939SharedAddress` (1 occurrences)

- **System.j1939SharedAddress**
  - Package: `M2::AUTOSARTemplates::SystemTemplate`
  - Kind: `attribute`, Multiplicity: `*`

### `ApplicationPartitionTo` (1 occurrences)

- **SystemMapping.application**
  - Package: `M2::AUTOSARTemplates::SystemTemplate`
  - Kind: `attribute`, Multiplicity: `*`

### `AppOsTaskProxyToEcu` (1 occurrences)

- **SystemMapping.appOsTask**
  - Package: `M2::AUTOSARTemplates::SystemTemplate`
  - Kind: `attribute`, Multiplicity: `*`

### `ComManagement` (1 occurrences)

- **SystemMapping.com**
  - Package: `M2::AUTOSARTemplates::SystemTemplate`
  - Kind: `attribute`, Multiplicity: `*`

### `DdsCpISignalToDds` (1 occurrences)

- **SystemMapping.ddsISignalTo**
  - Package: `M2::AUTOSARTemplates::SystemTemplate`
  - Kind: `attribute`, Multiplicity: `*`

### `RteEventInSystem` (1 occurrences)

- **SystemMapping.rteEventInSystem**
  - Package: `M2::AUTOSARTemplates::SystemTemplate`
  - Kind: `attribute`, Multiplicity: `*`

### `RteEventInSystemToOs` (1 occurrences)

- **SystemMapping.rteEventToOs**
  - Package: `M2::AUTOSARTemplates::SystemTemplate`
  - Kind: `attribute`, Multiplicity: `*`

### `SystemSignalGroupTo` (1 occurrences)

- **SystemMapping.systemSignalGroupTo**
  - Package: `M2::AUTOSARTemplates::SystemTemplate`
  - Kind: `attribute`, Multiplicity: `*`

### `SystemSignalTo` (1 occurrences)

- **SystemMapping.systemSignalTo**
  - Package: `M2::AUTOSARTemplates::SystemTemplate`
  - Kind: `attribute`, Multiplicity: `*`

### `MemoryAllocation` (1 occurrences)

- **SwAddrMethod.memory**
  - Package: `M2::MSR::DataDictionary::AuxillaryObjects`
  - Kind: `attribute`, Multiplicity: `0..1`

### `SectionInitialization` (1 occurrences)

- **SwAddrMethod.section**
  - Package: `M2::MSR::DataDictionary::AuxillaryObjects`
  - Kind: `attribute`, Multiplicity: `0..1`

### `BinaryManifestMeta` (1 occurrences)

- **CpSoftwareClusterBinaryManifestDescriptor.metaDataField**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SoftwareCluster::BinaryManifest`
  - Kind: `attribute`, Multiplicity: `*`

### `BinaryManifestProvide` (1 occurrences)

- **CpSoftwareClusterBinaryManifestDescriptor.provide**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SoftwareCluster::BinaryManifest`
  - Kind: `attribute`, Multiplicity: `*`

### `BinaryManifestRequire` (1 occurrences)

- **CpSoftwareClusterBinaryManifestDescriptor.require**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::SoftwareCluster::BinaryManifest`
  - Kind: `attribute`, Multiplicity: `*`

### `DiagnosticRequestFile` (1 occurrences)

- **DiagnosticRequestFileTransfer.requestFile**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::RequestFileTransfer`
  - Kind: `reference`, Multiplicity: `0..1`

### `SecurityEventReporting` (1 occurrences)

- **SecurityEventContextProps.default**
  - Package: `M2::AUTOSARTemplates::SecurityExtractTemplate`
  - Kind: `attribute`, Multiplicity: `0..1`

### `SymbolPropsName` (1 occurrences)

- **SecurityEventDefinition.eventSymbolName**
  - Package: `M2::AUTOSARTemplates::SecurityExtractTemplate`
  - Kind: `attribute`, Multiplicity: `0..1`

### `SecurityEvent` (1 occurrences)

- **SecurityEventFilterChain.aggregation**
  - Package: `M2::AUTOSARTemplates::SecurityExtractTemplate`
  - Kind: `attribute`, Multiplicity: `0..1`

### `SecurityEventOneEvery` (1 occurrences)

- **SecurityEventFilterChain.oneEveryN**
  - Package: `M2::AUTOSARTemplates::SecurityExtractTemplate`
  - Kind: `attribute`, Multiplicity: `0..1`

### `SecurityEventThreshold` (1 occurrences)

- **SecurityEventFilterChain.threshold**
  - Package: `M2::AUTOSARTemplates::SecurityExtractTemplate`
  - Kind: `attribute`, Multiplicity: `0..1`

### `SecurityEventFilter` (1 occurrences)

- **SecurityEventContextMapping.filterChain**
  - Package: `M2::AUTOSARTemplates::SecurityExtractTemplate`
  - Kind: `reference`, Multiplicity: `0..1`

### `IdsmModule` (1 occurrences)

- **IdsmInstance.idsmModule**
  - Package: `M2::AUTOSARTemplates::SecurityExtractTemplate`
  - Kind: `reference`, Multiplicity: `0..1`

### `IdsmSignatureSupport` (1 occurrences)

- **IdsmInstance.signature**
  - Package: `M2::AUTOSARTemplates::SecurityExtractTemplate`
  - Kind: `attribute`, Multiplicity: `0..1`

### `FlexrayFifo` (1 occurrences)

- **FlexrayCommunicationController.flexrayFifo**
  - Package: `M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Flexray::FlexrayTopology`
  - Kind: `attribute`, Multiplicity: `*`

### `EnumerationMapping` (1 occurrences)

- **EnumerationMappingTable.entry**
  - Package: `M2::AUTOSARTemplates::GenericStructure::VariantHandling::AttributeValueVariationPoints`
  - Kind: `attribute`, Multiplicity: `*`

### `OrientEnum` (1 occurrences)

- **Table.orient**
  - Package: `M2::MSR::Documentation::BlockElements::OasisExchangeTable`
  - Kind: `attribute`, Multiplicity: `0..1`

### `DiagnosticResponseOn` (1 occurrences)

- **DiagnosticResponseOnEvent.responseOn**
  - Package: `M2::AUTOSARTemplates::DiagnosticExtract::Dcm::DiagnosticService::ResponseOnEvent`
  - Kind: `reference`, Multiplicity: `0..1`

