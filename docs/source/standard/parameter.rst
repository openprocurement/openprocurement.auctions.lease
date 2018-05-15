.. . Kicking page rebuild 2014-10-30 17:00:08

.. index:: Parameter, LotValue, bidder, participant, pretendent

.. _Parameter:

Parameter
=========

Schema
------

:code:
    string, required

    Feature code.

:value:
    float, required

    Feature value.

.. _LotValue:

.. LotValue
   ========

   Schema
   ------

   :value:
    :ref:`Value`, required

    Validation rules:

    * `amount` should be less than `Lot.value.amout`
    * `currency` should either be absent or match `Lot.value.currency`
    * `valueAddedTaxIncluded` should either be absent or match `Lot.value.valueAddedTaxIncluded`

   :relatedLot:
    string

    ID of related :ref:`lot`.

   :date:
    string, :ref:`date`, auto-generated

   :participationUrl:
    URL

    A web address for participation in auction.
