from gpom.maps import GUIDMAP

class CAR(GUIDMAP):
    """Source: https://msdn.microsoft.com/ru-ru/library/cc223512.aspx

    5.1.3.2.1 Control Access Rights
In Active Directory, the implementer can control which users have the right to perform a particular operation on an object or its attributes by using standard access rights. However, there are certain operations that have semantics that are not tied to specific properties, or where it is desirable to control access in a way that is not supported by the standard access rights. For example, the implementer can grant users a "Reanimate tombstones" right so that they are able to perform tombstone reanimation on any object in a naming context. Active Directory allows the standard access control mechanism to be extended for controlling access to custom actions or operations, using a mechanism called control access rights.

A control access right is not identified by a specific bit in an access mask as the standard access rights are. Instead, each control access right is identified by a GUID. An ACE that grants or denies a control access right specifies the RIGHT_DS_CONTROL_ACCESS (CR) bit in the ACCESS_MASK field and the GUID identifying the particular control access right in the ObjectType field of the ACE. If the ObjectType field does not contain a GUID, the ACE is deemed to control the right to perform all operations associated with the objects that are controlled by control access rights. For convenience and easy identification by Active Directory administrative tools facilitating access control, each control access right is represented by an object of class controlAccessRight in the Extended-Rights container. Note that these objects are not integral to evaluating access to an operation and, therefore, their presence is not required for the proper functioning of the access control mechanism. There are a number of predefined control access rights in Active Directory, and that list can be extended by application developers by adding controlAccessRight objects to the Extended-Rights container.

The pertinent attributes on the controlAccessRight object that defines the use of the control access right for the administrative tools are as follows:

validAccesses: The type of access right bits in the ACCESS_MASK field of an ACE with which the control access right can be associated. The only permitted access right for control access rights is RIGHT_DS_CONTROL_ACCESS (CR).

rightsGuid: The GUID that is used to identify the control access right in an ACE. The GUID value is placed in the ObjectType field of the ACE.

appliesTo: This multivalue attribute has a list of object classes that the control access right applies to. Each object class in the list is represented by the schemaIDGUID attribute of the classSchema object that defines the object class in the Active Directory schema. The appliesTo values on the controlAccessRight are not enforced by the directory server; that is, the controlAccessRight can be included in security descriptors of objects of classes not specified in the appliesTo attribute.
    """

    def __init__(self):
        self.kind = 'ACE'
        self.m = [
            ('Abandon-Replication', 'ee914b82-0a98-11d1-adbb-00c04fd8d5cd'),
            ('Add-GUID', '440820ad-65b4-11d1-a3da-0000f875ae0d'),
            ('Allocate-Rids', '1abd7cf8-0a99-11d1-adbb-00c04fd8d5cd'),
            ('Allowed-To-Authenticate', '68b1d179-0d15-4d4f-ab71-46152e79a7bc'),
            ('Apply-Group-Policy', 'edacfd8f-ffb3-11d1-b41d-00a0c968f939'),
            ('Certificate-Enrollment', '0e10c968-78fb-11d2-90d4-00c04f79dc55'),
            ('Certificate-AutoEnrollment', 'a05b8cc2-17bc-4802-a710-e7c15ab866a2'),
            ('Change-Domain-Master', '014bf69c-7b3b-11d1-85f6-08002be74fab'),
            ('Change-Infrastructure-Master', 'cc17b1fb-33d9-11d2-97d4-00c04fd8d5cd'),
            ('Change-PDC', 'bae50096-4752-11d1-9052-00c04fc2d4cf'),
            ('Change-Rid-Master', 'd58d5f36-0a98-11d1-adbb-00c04fd8d5cd'),
            ('Change-Schema-Master', 'e12b56b6-0a95-11d1-adbb-00c04fd8d5cd'),
            ('Create-Inbound-Forest-Trust', 'e2a36dc9-ae17-47c3-b58b-be34c55ba633'),
            ('Do-Garbage-Collection', 'fec364e0-0a98-11d1-adbb-00c04fd8d5cd'),
            ('Domain-Administer-Server', 'ab721a52-1e2f-11d0-9819-00aa0040529b'),
            ('DS-Check-Stale-Phantoms', '69ae6200-7f46-11d2-b9ad-00c04f79f805'),
            ('DS-Execute-Intentions-Script', '2f16c4a5-b98e-432c-952a-cb388ba33f2e'),
            ('DS-Install-Replica', '9923a32a-3607-11d2-b9be-0000f87a36b2'),
            ('DS-Query-Self-Quota', '4ecc03fe-ffc0-4947-b630-eb672a8a9dbc'),
            ('DS-Replication-Get-Changes', '1131f6aa-9c07-11d1-f79f-00c04fc2dcd2'),
            ('DS-Replication-Get-Changes-All', '1131f6ad-9c07-11d1-f79f-00c04fc2dcd2'),
            ('DS-Replication-Get-Changes-In-Filtered-Set', '89e95b76-444d-4c62-991a-0facbeda640c'),
            ('DS-Replication-Manage-Topology', '1131f6ac-9c07-11d1-f79f-00c04fc2dcd2'),
            ('DS-Replication-Monitor-Topology', 'f98340fb-7c5b-4cdb-a00b-2ebdfa115a96'),
            ('DS-Replication-Synchronize' ,'1131f6ab-9c07-11d1-f79f-00c04fc2dcd2'),
            ('Enable-Per-User-Reversibly-Encrypted-Password', '05c74c5e-4deb-43b4-bd9f-86664c2a7fd5'),
            ('Generate-RSoP-Logging', 'b7b1b3de-ab09-4242-9e30-9980e5d322f7'),
            ('Generate-RSoP-Planning', 'b7b1b3dd-ab09-4242-9e30-9980e5d322f7'),
            ('Manage-Optional-Features', '7c0e2a7c-a419-48e4-a995-10180aad54dd'),
            ('Migrate-SID-History', 'ba33815a-4f93-4c76-87f3-57574bff8109'),
            ('msmq-Open-Connector', 'b4e60130-df3f-11d1-9c86-006008764d0e'),
            ('msmq-Peek', '06bd3201-df3e-11d1-9c86-006008764d0e'),
            ('msmq-Peek-computer-Journal', '4b6e08c3-df3c-11d1-9c86-006008764d0e'),
            ('msmq-Peek-Dead-Letter', '4b6e08c1-df3c-11d1-9c86-006008764d0e'),
            ('msmq-Receive', '06bd3200-df3e-11d1-9c86-006008764d0e'),
            ('msmq-Receive-computer-Journal', '4b6e08c2-df3c-11d1-9c86-006008764d0e'),
            ('msmq-Receive-Dead-Letter', '4b6e08c0-df3c-11d1-9c86-006008764d0e'),
            ('msmq-Receive-journal', '06bd3203-df3e-11d1-9c86-006008764d0e'),
            ('msmq-Send', '06bd3202-df3e-11d1-9c86-006008764d0e'),
            ('Open-Address-Book', 'a1990816-4298-11d1-ade2-00c04fd8d5cd'),
            ('Read-Only-Replication-Secret-Synchronization', '1131f6ae-9c07-11d1-f79f-00c04fc2dcd2'),
            ('Reanimate-Tombstones', '45ec5156-db7e-47bb-b53f-dbeb2d03c40f'),
            ('Recalculate-Hierarchy', '0bc1554e-0a99-11d1-adbb-00c04fd8d5cd'),
            ('Recalculate-Security-Inheritance', '62dd28a8-7f46-11d2-b9ad-00c04f79f805'),
            ('Receive-As', 'ab721a56-1e2f-11d0-9819-00aa0040529b'),
            ('Refresh-Group-Cache', '9432c620-033c-4db7-8b58-14ef6d0bf477'),
            ('Reload-SSL-Certificate', '1a60ea8d-58a6-4b20-bcdc-fb71eb8a9ff8'),
            ('Run-Protect_Admin_Groups-Task', '7726b9d5-a4b4-4288-a6b2-dce952e80a7f'),
            ('SAM-Enumerate-Entire-Domain', '91d67418-0135-4acc-8d79-c08e857cfbec'),
            ('Send-As', 'ab721a54-1e2f-11d0-9819-00aa0040529b'),
            ('Send-To', 'ab721a55-1e2f-11d0-9819-00aa0040529b'),
            ('Unexpire-Password', 'ccc2dc7d-a6ad-4a7a-8846-c04e3cc53501'),
            ('Update-Password-Not-Required-Bit', '280f369c-67c7-438e-ae98-1d46f3c6f541'),
            ('Update-Schema-Cache', 'be2bb760-7f46-11d2-b9ad-00c04f79f805'),
            ('User-Change-Password', 'ab721a53-1e2f-11d0-9819-00aa0040529b'),
            ('User-Force-Change-Password', '00299570-246d-11d0-a768-00aa006e0529'),
            ('DS-Clone-Domain-Controller', '3e0f7e18-2c7a-4c10-ba82-4d926db99a3e'),
            ('DS-Read-Partition-Secrets', '084c93a2-620d-4879-a836-f0ae47de0e89'),
            ('DS-Write-Partition-Secrets', '94825a8d-b171-4116-8146-1e34d8f54401'),
            ('DS-Set-Owner', '4125c71f-7fac-4ff0-bcb7-f09a41325286'),
            ('DS-Bypass-Quota', '88a9933e-e5c8-4f2a-9dd7-2527416b8092'),
            ('DS-Validated-Write-Computer', '9b026da6-0d3c-465c-8bee-5199d7165cba')
            ]
