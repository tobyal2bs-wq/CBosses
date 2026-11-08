"""Explicitly approved additions. Review-only drafts never enter this registry."""
import json,copy
from pathlib import Path
from models import model
from build import Model
APPROVED={'millstone_monk'}
INFO={'millstone_monk':dict(name='<gradient:#91b5aa:#e0d9bd><bold>Millstone Monk</bold></gradient>',title='Keeper of the Old Mill',entity='IRON_GOLEM',damage=12,armor=9,bar='GREEN',theme='earth',movement='walk',speed=.22,minion=None,minions=0,ability_seconds=8,phases=[.66,.33],hpp=.25,money=45000,top_money=135000,items=['STONE_BRICKS 32','MOSS_BLOCK 16','DIAMOND 2'],top_items=['NETHERITE_SCRAP 1'],extra=['heal'])}
def data(id):
 return json.loads((Path(__file__).parent/'approved'/(id+'.json')).read_text(encoding='utf8'))
@model
def millstone_monk():
 """An ancient stone millkeeper with a carved cyan-eyed face, moss-covered shoulders, folded robes, heavy braced hands and an axle-mounted turning millstone. The exposed glowing axle is its weak spot."""
 m=Model('millstone_monk','millstone',1)
 m.approved=data('millstone_monk')
 return m
