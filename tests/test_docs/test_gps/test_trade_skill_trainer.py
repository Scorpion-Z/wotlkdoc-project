# -*- coding: utf-8 -*-

import pytest
from wotlkdoc.docs.gps.trade_skill_trainer import lt_list_trade_skill_trainer_gsp


def test():
    lt = lt_list_trade_skill_trainer_gsp()
    lt.render()
    # print(lt.render())


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
