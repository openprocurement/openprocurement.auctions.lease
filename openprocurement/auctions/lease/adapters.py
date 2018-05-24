# -*- coding: utf-8 -*-
from datetime import timedelta
from openprocurement.auctions.core.adapters import AuctionConfigurator, AuctionManagerAdapter
from openprocurement.auctions.lease.models import (
    propertyLease,
)
from openprocurement.auctions.core.plugins.awarding.v2_1.adapters import (
    AwardingV2_1ConfiguratorMixin
)
from openprocurement.auctions.core.utils import (
    SANDBOX_MODE, TZ, calculate_business_date, get_request_from_root, get_now,
)
from openprocurement.api.utils import set_specific_hour
from .utils import generate_rectificationPeriod
from .constants import ADDITIONAL_LEASE_CLASSIFICATION_MANDATORY


class AuctionLeaseConfigurator(AuctionConfigurator, AwardingV2_1ConfiguratorMixin):
    name = 'Auction Lease Configurator'
    model = propertyLease


class AuctionLeaseManagerAdapter(AuctionManagerAdapter):

    def create_auction(self, request):
        auction = request.validated['auction']
        now = get_now()
        start_date = TZ.localize(auction.auctionPeriod.startDate.replace(tzinfo=None))
        pause_between_periods = start_date - (set_specific_hour(start_date, hour=20) - timedelta(days=1))
        end_date = calculate_business_date(start_date, -pause_between_periods, auction)
        four_workingDays_before_startDate = calculate_business_date(auction.auctionPeriod.startDate, -timedelta(days=4), auction, working_days=True, specific_hour=20)
        if auction.tenderPeriod and auction.tenderPeriod.endDate:
            if auction.tenderPeriod.endDate.date() != four_workingDays_before_startDate.date():
                request.errors.add('body', 'data', 'the pause between tenderPeriod.endDate and auctionPeriod.startDate should be either 3 or 0 days')
                request.errors.status = 422
            else:
                auction.tenderPeriod.startDate = now
                auction.tenderPeriod.endDate = four_workingDays_before_startDate
        else:
            auction.tenderPeriod = type(auction).tenderPeriod.model_class()
            auction.tenderPeriod.startDate = now
            auction.tenderPeriod.endDate = end_date
        if not auction.enquiryPeriod:
            auction.enquiryPeriod = type(auction).enquiryPeriod.model_class()
        auction.enquiryPeriod.startDate = now
        auction.enquiryPeriod.endDate = end_date
        if not auction.rectificationPeriod:
            auction.rectificationPeriod = generate_rectificationPeriod(auction)
        auction.rectificationPeriod.startDate = now
        auction.date = now
        auction.auctionPeriod.startDate = None
        auction.auctionPeriod.endDate = None
        if auction.lots:
            for lot in auction.lots:
                lot.date = now

        for item in auction['items']:
            lease_classification_added = False
            for additionalClassification in item['additionalClassifications']:
                if (additionalClassification['scheme'] == u'CPVS' and additionalClassification['id'] == u'PA01-7'):
                    lease_classification_added = True
            if not lease_classification_added:
                item['additionalClassifications'].append(ADDITIONAL_LEASE_CLASSIFICATION_MANDATORY)


    def change_auction(self, request):
        pass
