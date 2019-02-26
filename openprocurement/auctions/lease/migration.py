# -*- coding: utf-8 -*-
import logging

from openprocurement.auctions.core.plugins.awarding.v2_1.migration import (
    migrate_awarding_1_0_to_awarding_2_1
)
from openprocurement.auctions.core.utils import migrate_all_document_of_tender
from openprocurement.api.migration import (
    BaseMigrationsRunner,
    BaseMigrationStep,
    MigrationResourcesDTO,
    AliasesInfoDTO
)

from openprocurement.auctions.lease.models import Auction


LOGGER = logging.getLogger(__name__)
SCHEMA_VERSION = 1
SCHEMA_DOC = 'openprocurement_auctions_dgf_schema'
PACKAGE_ALIASES = {
    'openprocurement.auctions.lease': ['propertyLease', 'leaseFinancial']
}


class LeaseMigrationsRunner(BaseMigrationsRunner):

    SCHEMA_VERSION = SCHEMA_VERSION
    SCHEMA_DOC = SCHEMA_DOC


class MigrateAwardingStep(BaseMigrationStep):

    def setUp(self):
        self.view = 'auctions/all'
        self.procurement_method_types = self.resources.aliases_info.get_package_aliases(
            'openprocurement.auctions.lease'
        )

    def migrate_document(self, auction):
        if auction['procurementMethodType'] in self.procurement_method_types:
            migrate_awarding_1_0_to_awarding_2_1(auction, self.procurement_method_types)
            auction = Auction(auction)
            auction = auction.to_primitive()
            return auction
        return None


class DocumentOfStep(BaseMigrationStep):

    def setUp(self):
        self.view = 'auctions/all'
        self.procurement_method_types = self.resources.aliases_info.get_package_aliases(
            'openprocurement.auctions.lease'
        )

    def migrate_document(self, auction):
        if auction['procurementMethodType'] in self.procurement_method_types:
            changed = migrate_all_document_of_tender(auction)
            return auction if changed else None
        return None


MIGRATION_STEPS = (MigrateAwardingStep, DocumentOfStep)


def migrate(db):
    aliases_info_dto = AliasesInfoDTO(PACKAGE_ALIASES)
    migration_resource_dto = MigrationResourcesDTO(db, aliases_info_dto)
    runner = LeaseMigrationsRunner(migration_resource_dto)
    runner.migrate(MIGRATION_STEPS)
