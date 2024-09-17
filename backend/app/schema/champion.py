from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, AliasChoices, Extra

from app.schema.utils import convert_string


class StatsValue(BaseModel):
    flat: float
    per_level: float


class Stats(BaseModel):
    health: StatsValue
    health_regen: StatsValue
    mana: StatsValue
    mana_regen: StatsValue
    move_speed: StatsValue
    armor: StatsValue
    magic_resistance: StatsValue
    attack_range: StatsValue
    crit: StatsValue
    attack_damage: StatsValue
    attack_speed: StatsValue
    missile_speed: Optional[float]
    attack_cast_time: Optional[float] = None
    attack_total_time: Optional[float] = None
    attack_delay_offset: Optional[float]
    acquisition_radius: float
    selection_radius: float
    gameplay_radius: float
    pathing_radius: float
    aram_dmg_dealt: float
    aram_dmg_taken: float
    aram_healing: Optional[float]
    aram_shielding: Optional[float]
    urf_dmg_dealt: float
    urf_dmg_taken: float
    urf_healing: Optional[float]
    urf_shielding: Optional[float]


class Spells(BaseModel):
    key: str
    name: str
    description: str
    icon: str
    max_rank: int
    cooldown: List[float]
    cast_time: Optional[None | List[float | str | None]] = None
    range: List[float]
    first_cast_damage: Optional[List[float]] = None
    second_cast_damage: Optional[List[float]] = None
    third_cast_damage: Optional[List[float]] = None
    maximum_non_minion_damage: Optional[List[float]] = Field(default=None, alias='maximum_non-minion_damage')
    explanation: Optional[List[str]] = None
    cost: List[float]
    width: Optional[List[float | None] | float] = None
    speed: Optional[List[float | str | None] | str | float] = None
    magic_damage: Optional[List[float]] = None
    slow: Optional[List[float]] = None
    total_damage: Optional[List[float]] = None
    target_range: Optional[float | List[float | None] | str] = None
    effect_radius: Optional[float | str | List[float | str | None]] = None
    bonus_movement_speed: Optional[List[float]] = None
    bonus_attack_damage: Optional[List[float]] = None
    increased_healing: Optional[List[float]] = None
    damage_per_pass: Optional[List[float]] = None
    initial_flame_magic_damage: Optional[List[float]] = None
    increased_initial_flame_minion_damage: Optional[List[float]] = None
    disable_duration: Optional[List[float]] = None
    angle: Optional[List[float]] = None
    shroud_duration: Optional[List[float]] = None
    collision_radius: Optional[List[float]] = None
    minimum_magic_damage: Optional[List[float]] = None
    physical_damage: Optional[List[float | None] | None] = None
    total_physical_damage: Optional[List[float]] = None
    non_champion_damage: Optional[List[float]] = Field(default=None, alias='non-champion_damage')
    detection_radius: Optional[float] = None
    physical_damage_per_shot: Optional[List[float]] = None
    maximum_bullets_stored: Optional[List[float]] = None
    minimum_physical_damage_per_bullet: Optional[List[float]] = None
    magic_damage_per_tick: Optional[List[float]] = None
    damage_reduction: Optional[List[float]] = None
    static_cooldown: Optional[List[float | str]] = None
    recharge: Optional[List[float]] = None
    physical_damage_reduction: Optional[List[float]] = None
    stun_duration: Optional[List[float]] = None
    number_of_ice_segments: Optional[List[float]] = None
    tether_radius: Optional[List[float]] = None
    empowered_damage_per_tick: Optional[List[float]] = None
    empowered_slow: Optional[List[float]] = None
    shield_strength: Optional[List[float]] = None
    initial_magic_damage: Optional[List[float]] = None
    bonus_attack_speed: Optional[List[float]] = None
    physical_damage_per_arrow: Optional[List[float]] = None
    arrows: Optional[List[float]] = None
    reduced_damage: Optional[List[float]] = None
    initial_cost: Optional[List[float]] = None
    total_maximum_magic_damage: Optional[List[float]] = None
    bonus_magic_damage: Optional[List[float]] = None
    breath_of_light_flat_damage_modifier: Optional[List[float]] = None
    inner_radius: Optional[float | str] = None
    subsequent_bolt_minimum_magic_damage: Optional[List[float]] = None
    invisibility_duration: Optional[List[float]] = None
    rift_duration: Optional[List[float]] = None
    minimum_heal: Optional[List[float]] = None
    per_direction_cooldown: Optional[List[float]] = Field(default=None, alias='per-direction_cooldown')
    monster_bonus_physical_damage: Optional[List[float]] = None
    modified_minion_damage: Optional[List[float]] = None
    slow_duration: Optional[List[float]] = None
    minimum_physical_damage_per_hit: Optional[List[float]] = None
    minimum_monster_damage_per_hit: Optional[List[float]] = None
    bonus_true_damage: Optional[List[float]] = None
    maximum_monster_damage: Optional[List[float]] = None
    true_damage: Optional[List[float]] = None
    bonus_health: Optional[List[float]] = None
    increased_total_attack_speed: Optional[List[float]] = None
    heal: Optional[List[float]] = None
    initial_bonus_movement_speed: Optional[List[float]] = None
    increased_damage: Optional[List[float]] = None
    ally_bonus_armor: Optional[List[float]] = None
    ally_bonus_magic_resistance: Optional[List[float]] = None
    self_bonus_armor: Optional[List[float]] = None
    self_bonus_magic_resistance: Optional[List[float]] = None
    barrier_duration: Optional[List[float]] = None
    maximum_knockup_duration: Optional[List[float]] = None
    resistances_reduction: Optional[List[float]] = None
    heal_per_tick: Optional[List[float]] = None
    maximum_magic_damage: Optional[List[float]] = None
    total_magic_damage: Optional[List[float]] = None
    life_steal: Optional[List[float]] = None
    additional_bonus_movement_speed: Optional[List[float]] = None
    trap_duration: Optional[List[float]] = None
    maximum_number_of_traps: Optional[List[float]] = None
    headshot_damage_increase: Optional[List[float]] = None
    bonus_physical_damage: Optional[List[float]] = None
    increased_mixed_damage: Optional[List[float]] = None
    outer_cone_bonus_damage: Optional[List[float]] = None
    non_epic_monster_damage: Optional[List[float]] = Field(default=None, alias='non-epic_monster_damage')
    bonus_non_epic_monster_damage: Optional[List[float]] = Field(default=None, alias='bonus_non-epic_monster_damage')
    zone_duration: Optional[List[float]] = None
    magic_damage_per_second: Optional[List[float]] = None
    silence_duration: Optional[List[float]] = None
    champion_true_damage: Optional[List[float]] = None
    non_champion_true_damage: Optional[List[float]] = Field(default=None, alias='non-champion_true_damage')
    bonus_health_per_stack: Optional[List[float]] = None
    bonus_attack_range_per_stack: Optional[List[float]] = None
    bonus_size_per_stack: Optional[List[float]] = None
    physical_damage_per_tick: Optional[List[float]] = None
    resistances_reduction_per_stack: Optional[List[float]] = None
    big_one_physical_damage: Optional[List[float]] = None
    armor_penetration: Optional[List[float]] = None
    magic_damage_per_orb: Optional[List[float]] = None
    maximum_shield_strength: Optional[List[float]] = None
    bonus_damage_per_champion: Optional[List[float]] = None
    minimum_physical_damage: Optional[List[float]] = None
    minimum_damage: Optional[List[float]] = None
    capped_monster_damage: Optional[List[float]] = None
    minimum_bonus_physical_damage: Optional[List[float]] = None
    increased_base_health: Optional[List[float]] = None
    bonus_health_regeneration: Optional[List[float]] = None
    barrage_cooldown: Optional[List[float]] = None
    magic_resistance_reduction: Optional[List[float]] = None
    monster_disable_duration: Optional[List[float]] = None
    empowered_damage: Optional[List[float]] = None
    target_immunity: Optional[List[float] | float] = None
    fear_duration: Optional[List[float]] = None
    increased_magic_damage: Optional[List[float]] = None
    increased_minimum_damage: Optional[List[float]] = None
    champion_heal_percentage: Optional[List[float]] = None
    critical_damage: Optional[List[float]] = None
    mana_restored: Optional[List[float]] = None
    bonus_magic_damage_on_hit: Optional[List[float]] = Field(default=None, alias='bonus_magic_damage_on-hit')
    guppy_damage: Optional[List[float]] = None
    chomper_damage: Optional[List[float]] = None
    gigalodon_damage: Optional[List[float]] = None
    magic_shield_strength: Optional[List[float]] = None
    magic_damage_reduction: Optional[List[float]] = None
    gold_plunder: Optional[List[float]] = None
    silver_serpent_plunder: Optional[List[float]] = None
    maximum_charges: Optional[List[float]] = None
    bonus_champion_damage: Optional[List[float]] = None
    magic_damage_per_wave: Optional[List[float]] = None
    true_damage_with__deaths_daughter: Optional[List[float]] = Field(default=None,
                                                                     alias="true_damage_with__death's_daughter")
    total_mixed_damage_with__deaths_daughter: Optional[List[float]] = Field(default=None,
                                                                            alias="total_mixed_damage_with__death's_daughter")
    total_magic_damage_with__fire_at_will: Optional[List[float]] = None
    maximum_mixed_total_damage_with__fire_at_will_and__deaths_daughter: Optional[List[float]] = Field(
        default=None, alias="maximum_mixed_total_damage_with__fire_at_will_and__death's_daughter"
    )
    movement_speed_duration: Optional[List[float]] = None
    physical_damage_per_spin: Optional[List[float]] = None
    increased_damage_per_spin: Optional[List[float]] = None
    hyper_bonus_movement_speed: Optional[List[float]] = None
    minimum_minion_damage: Optional[List[float]] = None
    minimum_slow: Optional[List[float]] = None
    sight_reduction: Optional[List[float]] = None
    bonus_armor: Optional[List[float]] = None
    damage_per_snip: Optional[List[float]] = None
    final_snip_damage: Optional[List[float]] = None
    maximum_damage: Optional[List[float]] = None
    bonus_resistances: Optional[List[float]] = None
    cooldown_refund: Optional[List[float]] = None
    magic_damage_per_needle: Optional[List[float]] = None
    reduced_slow: Optional[List[float]] = None
    second_cast_total_damage: Optional[List[float]] = None
    capped_healing: Optional[List[float]] = None
    additional_magic_damage: Optional[List[float]] = None
    additional_minion_damage: Optional[List[float]] = None
    damage_increase: Optional[List[float]] = None
    damage_transmission: Optional[List[float]] = None
    flat_cooldown_reduction: Optional[List[float]] = None
    root_duration: Optional[List[float]] = None
    ally_bonus_magic_damage: Optional[List[float]] = None
    bonus_damage_per_second: Optional[List[float]] = None
    armor_reduction: Optional[List[float]] = None
    impassable_perimeter: Optional[str | List[float | str| None]] = None
    minimum_fourth_shot_damage: Optional[List[float]] = None
    bonus_range: Optional[List[float]] = None
    maximum_physical_damage: Optional[List[float]] = None
    maximum_secondary_damage: Optional[List[float]] = None
    physical_damage_per_missile: Optional[List[float]] = None
    reduced_damage_per_missile: Optional[List[float]] = None
    total_evolved_single_target_damage: Optional[List[float]] = Field(default=None,
                                                                      alias='total_evolved_single-target_damage')
    minimum_movement_speed: Optional[List[float]] = None
    maximum_non_champion_damage: Optional[List[float]] =  Field(default=None, alias='maximum_non-champion_damage')
    knock_up_duration: Optional[List[float]] = None
    wall_length: Optional[List[float]] = None
    increased_bonus_magic_damage: Optional[List[float]] = None
    bonus_damage_per_stack: Optional[List[float]] = None
    physical_damage_per_dagger: Optional[List[float]] = None
    magic_damage_per_dagger: Optional[List[float]] = None
    on_attack_on_hit_effectiveness: Optional[List[float]] =  Field(default=None, alias='on-attack/on-hit_effectiveness')
    passive_damage: Optional[List[float]] = None
    capped_monster_damage_per_hit: Optional[List[float]] = None
    duration: Optional[List[float]] = None
    magic_damage_per_bolt: Optional[List[float]] = None
    total_single_target_damage: Optional[List[float]] = Field(default=None, alias='total_single-target_damage')
    additional_physical_damage: Optional[List[float]] = None
    minimum_shield: Optional[List[float]] = None
    bonus_attack_range: Optional[List[float]] = None
    additional_damage: Optional[List[float]] = None
    healing_percentage: Optional[List[float]] = None
    collision_physical_damage: Optional[List[float]] = None
    flat_damage_reduction: Optional[List[float]] = None
    bonus_magic_resistance: Optional[List[float]] = None
    minion_damage: Optional[List[float]] = None
    sleep_duration: Optional[List[float]] = None
    minimum_heal_per_tick: Optional[List[float]] = None
    minimum_total_heal: Optional[List[float]] = None
    minion_damage_per_shot: Optional[List[float]] = None
    reduced_minion_damage: Optional[List[float]] = None
    effect_duration: Optional[List[float]] = None
    cripple: Optional[List[float]] = None
    voidling_duration: Optional[List[float]] = None
    bonus_monster_damage: Optional[List[float]] = None
    total_enhanced_damage: Optional[List[float]] = None
    monster_bonus_damage: Optional[List[float]] = None
    modified_damage_reduction: Optional[List[float]] = None
    base_attack_range_scaling: Optional[List[float]] = None
    increased_bonus_movement_speed: Optional[List[float]] = None
    total_waves: Optional[List[float]] = None
    wave_interval_time: Optional[List[float]] = None
    clone_outgoing_damage: Optional[List[float]] = None
    maximum_total_physical_damage: Optional[List[float]] = None
    shield_to_healing: Optional[List[float]] = None
    magic_penetration: Optional[List[float]] = None
    minimum_damage_per_tick: Optional[List[float]] = None
    minimum_total_damage: Optional[List[float]] = None
    initial_physical_damage: Optional[List[float]] = None
    bleed_physical_damage_per_tick: Optional[List[float]] = None
    minimum_total_physical_damage: Optional[List[float]] = None
    packmate_physical_damage: Optional[List[float]] = None
    dash_physical_damage: Optional[List[float]] = None
    flurry_physical_damage: Optional[List[float]] = None
    extra__packmates_summoned: Optional[List[float]] = None
    bonus_magic_damage_per_hit: Optional[List[float]] = None
    maximum_slow: Optional[List[float]] = None
    maximum_cripple: Optional[List[float]] = None
    increased_size: Optional[List[float]] = None
    monster_damage: Optional[List[float]] = None
    empowered_root_duration: Optional[List[float]] = None
    burst_physical_damage: Optional[List[float]] = None
    base_non_champion_heal: Optional[List[float]] = Field(default=None, alias='base_non-champion_heal')
    champion_magic_damage: Optional[List[float]] = None
    base_champion_heal: Optional[List[float]] = None
    size_radius: Optional[List[float]] = None
    minimum_reduced_damage: Optional[List[float]] = None
    magic_damage_per_hit: Optional[List[float]] = None
    maximum_total_magic_damage: Optional[List[float]] = None
    movement_speed_modifier: Optional[List[float]] = None
    total_minimum_minion_damage: Optional[List[float]] = Field(default=None, alias='total_minimum/minion_damage')
    total_monster_damage: Optional[List[float]] = None
    hurl_physical_damage: Optional[List[float]] = None
    hurl_secondary_physical_damage: Optional[List[float]] = None
    thrust_physical_damage: Optional[List[float]] = None
    capped_monster_health_damage: Optional[List[float]] = None
    total_movement_speed_increase: Optional[List[float]] = None
    taunt_bonus_attack_speed_duration: Optional[List[float]] = Field(default=None,
                                                                     alias='taunt/bonus_attack_speed_duration')
    center_minimum_damage: Optional[List[float]] = None
    berserk_duration: Optional[List[float]] = None
    healing_cap: Optional[List[float]] = None
    non_champion_healing: Optional[List[float]] = Field(default=None, alias='non-champion_healing')
    champion_healing: Optional[List[float]] = None
    empowered_bonus_damage: Optional[List[float]] = None
    total_minion_damage: Optional[List[float]] = None
    total_enhanced_minion_damage: Optional[List[float]] = None
    enhanced_shield_strength: Optional[List[float]] = None
    enhanced_bonus_movement_speed: Optional[List[float]] = None
    enhanced_damage: Optional[List[float]] = None
    enhanced_magic_resistance_reduction: Optional[List[float]] = None
    enhanced_slow: Optional[List[float]] = None
    bonus_overload_damage: Optional[List[float]] = None
    physical_damage_per_hit: Optional[List[float]] = None
    healing: Optional[List[float]] = None
    maximum_champion_damage: Optional[List[float]] = None
    heal_per_ally: Optional[List[float]] = None
    damage: Optional[List[float]] = None
    monster_physical_damage: Optional[List[float]] = None
    modified_magic_damage: Optional[List[float]] = None
    increased_bonus_damage: Optional[List[float]] = None
    minimum_shield_strength: Optional[List[float]] = None
    fury_generation_per_second: Optional[List[float]] = None
    size_increase: Optional[List[float]] = None
    bonus_stats: Optional[List[float]] = None
    regeneration_per_second: Optional[List[float]] = None
    maximum_base_damage_increase: Optional[List[float]] = None
    minimum_monster_damage: Optional[List[float]] = None
    total_maximum_champion_damage: Optional[List[float]] = None
    bounce_damage: Optional[List[float]] = None
    minion_bounce_damage: Optional[List[float]] = None
    glob_physical_damage: Optional[List[float]] = None
    explosion_physical_damage: Optional[List[float]] = None
    glob_non_champion_damage: Optional[List[float]] = Field(default=None, alias='glob_non-champion_damage')
    explosion_non_champion_damage: Optional[List[float]] = Field(default=None, alias='explosion_non-champion_damage')
    self_heal: Optional[List[float]] = None
    minimum_damage_mitigated: Optional[List[float]] = None
    total_heal: Optional[List[float]] = None
    health_cost_reduction: Optional[List[float]] = None
    bonus_damage_per_bolt: Optional[List[float]] = None
    reveal_duration: Optional[List[float]] = None
    on_target_cooldown: Optional[List[float]] = Field(default=None, alias='on-target_cooldown')
    ability_haste: Optional[List[float]] = None
    magic_damage_per_sphere: Optional[List[float]] = None
    damage_stored_into_grey_health: Optional[List[float]] = None
    increased_damage_stored_into_grey_health: Optional[List[float]] = None
    detonation_magic_damage: Optional[List[float]] = None
    total_maximum_detonation_damage: Optional[List[float]] = None
    on_terrain_cooldown: Optional[List[float]] = Field(default=None, alias='on-terrain_cooldown')
    blind_duration: Optional[List[float]] = None
    increased_blind_duration: Optional[List[float]] = None
    bounce_distance_cap: Optional[List[float]] = None
    minimum_bonus_magic_damage: Optional[List[float]] = None
    maximum_bonus_magic_damage: Optional[List[float]] = None
    side_length: Optional[List[float]] = None
    knock_back_distance: Optional[List[float]] = None
    attack_damage_reduction: Optional[List[float]] = None
    pillar_radius: Optional[List[float]] = None
    additional_bonus_ad: Optional[List[float]] = None
    fury_gained: Optional[List[float]] = None
    minimum_health_threshold: Optional[List[float]] = None
    stealth_duration: Optional[List[float]] = None
    base_physical_damage: Optional[List[float]] = None
    physical_damage_per_stack: Optional[List[float]] = None
    bonus_physical_damage_on_hit: Optional[List[float]] = Field(default=None, alias='bonus_physical_damage_on-hit')
    increased_shield_strength: Optional[List[float]] = None
    total_healing: Optional[List[float]] = None
    increased_life_steal: Optional[List[float]] = None
    decayed_bonus_movement_speed: Optional[List[float]] = None
    increased_slow: Optional[List[float]] = None
    modified_physical_damage: Optional[List[float]] = None
    bonus_magic_damage_per_stack: Optional[List[float]] = None
    maximum_bonus_magic_damage_per_stack: Optional[List[float]] = None
    active_magic_damage: Optional[List[float]] = None
    tumble_cooldown_reduction: Optional[List[float]] = None
    mana_restored_per_kill: Optional[List[float]] = None
    damage_per_tick: Optional[List[float]] = None
    minimum_bonus_damage: Optional[List[float]] = None
    turret_disable_duration: Optional[List[float]] = None
    increased_attack_speed: Optional[List[float]] = None
    increased_movement_speed: Optional[List[float]] = None
    reduced_damage_per_hit: Optional[List[float]] = None
    physical_damage_per_feather: Optional[List[float]] = None
    mana_refunded: Optional[List[float]] = None
    number_of_recasts: Optional[List[float]] = None
    maximum_stacks: Optional[List[float]] = None
    increased_damage_per_stack: Optional[List[float]] = None
    distance: Optional[List[float]] = None
    slash_physical_damage: Optional[List[float]] = None
    wall_width: Optional[List[float]] = None
    total_mixed_damage: Optional[List[float]] = None
    damage_stored: Optional[List[float]] = None
    wall_health: Optional[List[float]] = None
    mist_walkers: Optional[List[float]] = None
    heal_and_shield_power: Optional[List[float]] = None
    healing_on_hit: Optional[List[float]] = Field(default=None, alias='healing_on-hit')
    shield: Optional[List[float]] = None
    minimum_mana_restored: Optional[List[float]] = None
    heal_per_hit: Optional[List[float]] = None
    best_friend_heal_per_hit: Optional[List[float]] = None
    capped_non_champion_damage: Optional[List[float]] = Field(default=None, alias='capped_non-champion_damage')
    maximum_range_channel_duration: Optional[List[float]] = None
    energy_restored: Optional[List[float]] = None
    burst_fire_bonus_magic_damage: Optional[List[float]] = None
    burst_fire_modified_secondary_damage: Optional[List[float]] = None
    demolition_threshold: Optional[List[float]] = None
    magic_damage_per_mine: Optional[List[float]] = None
    bonus_movement_speed_duration: Optional[List[float]] = None
    bonus_damage_cap: Optional[List[float]] = None

    @field_validator('speed', mode='before')
    def validate_speed(cls, value):
        if not value:
            return None
        if isinstance(value, (float, str)):
            return [value]
        return value

    @field_validator(
        'target_range', 'width', 'cast_time', 'physical_damage', 'angle', 'barrage_cooldown',
        'sight_reduction', 'pillar_radius', 'side_length', 'recharge', 'collision_radius', 'on_target_cooldown',
        'tether_radius',
        mode='before'
    )
    def validate_list(cls, value):
        if not value or value is None:
            return None
        elif isinstance(value, (float, int)):
            return [value]
        return [convert_string(v) if v else None for v in value]

    @field_validator('static_cooldown', 'effect_radius', mode='before')
    def validate_list_str(cls, value):
        if not value:
            return None
        elif isinstance(value, (float, int, str)):
            return [value]
        return value

    @field_validator('impassable_perimeter', mode='before')
    def validate_impassable_perimeter(cls, value):
        if not value:
            return None
        elif isinstance(value, str):
            return value.split(' ')
        return [float(v) if v else None for v in value]


class Price(BaseModel):
    blue_essence: float = Field(validation_alias=AliasChoices('blue_essence', 'blueEssence'))
    rp: float
    sale_rp: float = Field(validation_alias=AliasChoices('sale_rp', 'saleRp'))


class Rarities(BaseModel):
    rarity: Optional[float]
    region: Optional[str]


class Chromas(BaseModel):
    id: str
    name: str
    icon: str


class Skins(BaseModel):
    id: int
    is_base: bool
    name: str
    splash: str
    icon: str
    chroma_icon: Optional[str]
    chromas: List
    cost: Optional[int | str] = None
    release_date: Optional[datetime] = None
    voice_actor: Optional[List[str]] = None
    splash_artist: Optional[List[str]] = None
    lore: Optional[str] = None

    @field_validator('release_date', mode='before')
    def validate_release(cls, value):
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                return None
        return value


class Passive(BaseModel):
    name: str
    description: str
    icon: str
    static_cooldown: Optional[List[float]] = None
    explanation: Optional[List[str]] = None
    effect_radius: Optional[List[float | str]] = None
    speed: Optional[List[float | str | None]] = None
    target_range: Optional[List[float]] = None
    tether_radius: Optional[List[float]] = None
    target_immunity: Optional[List[float]] = None
    detection_radius: Optional[List[float]] = None
    angle: Optional[List[float]] = None
    range: Optional[List[float]] = None
    width: Optional[List[float]] = None
    leash_range: Optional[List[float]] = None
    forge_disable_time: Optional[List[float]] = None
    cooldown: Optional[List[float]] = None
    per_leg_cooldown: Optional[List[float]] = Field(default=None, alias='per-leg_cooldown')
    attack_range: Optional[List[float]] = None

    @field_validator(
        'effect_radius',
        'static_cooldown', 'speed', 'attack_range', 'tether_radius', 'detection_radius', 'range', 'target_immunity',
        'width', 'angle', 'forge_disable_time', 'target_range',
        mode='before'
    )
    def validate_list(cls, value):
        if not value:
            return None
        elif isinstance(value, float):
            return [value]
        return [v if v else None for v in value]


class Tactical(BaseModel):
    damage: float
    toughness: float
    control: float
    mobility: float
    utility: float
    difficulty: float


class Items(BaseModel):
    name: str
    number: Optional[int]


class Build(BaseModel):
    name: str
    items: List[Items]


class RecommendedItems(BaseModel):
    name: str
    build: List[Build]


class Playstyle(BaseModel):
    ability_name: Optional[str] = None
    ability_text: List[str]


class Runes(BaseModel):
    perks: Optional[str] = None
    keystone: Optional[List[str]] = None
    text: Optional[str] = None


class TricksValue(BaseModel):
    title: Optional[str] = None
    text: Optional[List[str]] = None


class Tricks(BaseModel):
    title: Optional[str] = None
    value: List[TricksValue]


class ChampionCreate(BaseModel):
    champ_id: int
    patch: str

    name: str
    title: str
    icon: str
    resource: str
    release_date: datetime
    release_patch: str
    role: List[str]
    adaptive_type: str
    range_type: str
    blue_essence: int
    rp: int

    ally_tips: Optional[List[str]] = None
    enemy_tips: Optional[List[str]] = None
    team_mate_tips: Optional[List[str]] = None

    tactical: Tactical
    stats: Stats
    spells: List[Spells]
    passive: Passive
    skins: List[Skins]
    recommended_items: Optional[List[RecommendedItems]] = None
    playstyle: Optional[List[Playstyle]] = None
    runes: Optional[List[Runes]] = None
    items: Optional[List[str]] = None
    tricks: Optional[List[Tricks]] = None
    biography: List[str]

    @field_validator('release_date', mode='before')
    def validate_date(cls, value):
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                return None
        return value


class GetChampion(BaseModel):
    id: str

    class Config:
        extra = Extra.allow


class ListChampion(BaseModel):
    id: str
    champ_id: int
    name: str
