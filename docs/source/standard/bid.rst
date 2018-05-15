.. . Kicking page rebuild 2014-10-30 17:00:08

.. index:: Bid, bidder, participant, pretendent

.. _bid:

Bid
===

Schema
------

:status:
    string, default='active'

    Possible values are:

    * `draft`
    * `active`

:tenderers:
    List of :ref:`Organization` objects, required

:documents:
    List of :ref:`Document` objects, default='empty list'

:qualified:
    bool, required

:date:
    string, :ref:`date`, auto-generated
    
    Date when bid has been submitted.

:id:
    UID, auto-generated

:value:
    :ref:`Value`, required

    Validation rules:

    * ``amount`` should be less than ``Auction.value.amout``
    * ``currency`` should either be absent or match ``Auction.value.currency``
    * ``valueAddedTaxIncluded`` should either be absent or match ``Auction.value.valueAddedTaxIncluded``

:parameters:
    List of :ref:`Parameter` objects

.. ASK:lotValues:
    List of :ref:`LotValue` objects

:participationUrl:
    URL

    A web address for participation in auction.

:eligible:
    bool
