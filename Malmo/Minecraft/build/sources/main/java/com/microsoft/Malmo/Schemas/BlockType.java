//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, v2.2.4 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2018.05.03 at 04:13:26 PM CEST 
//


package com.microsoft.Malmo.Schemas;

import javax.xml.bind.annotation.XmlEnum;
import javax.xml.bind.annotation.XmlEnumValue;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for BlockType.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * <p>
 * <pre>
 * &lt;simpleType name="BlockType">
 *   &lt;restriction base="{http://www.w3.org/2001/XMLSchema}string">
 *     &lt;enumeration value="air"/>
 *     &lt;enumeration value="stone"/>
 *     &lt;enumeration value="grass"/>
 *     &lt;enumeration value="dirt"/>
 *     &lt;enumeration value="cobblestone"/>
 *     &lt;enumeration value="planks"/>
 *     &lt;enumeration value="sapling"/>
 *     &lt;enumeration value="bedrock"/>
 *     &lt;enumeration value="flowing_water"/>
 *     &lt;enumeration value="water"/>
 *     &lt;enumeration value="flowing_lava"/>
 *     &lt;enumeration value="lava"/>
 *     &lt;enumeration value="sand"/>
 *     &lt;enumeration value="gravel"/>
 *     &lt;enumeration value="gold_ore"/>
 *     &lt;enumeration value="iron_ore"/>
 *     &lt;enumeration value="coal_ore"/>
 *     &lt;enumeration value="log"/>
 *     &lt;enumeration value="leaves"/>
 *     &lt;enumeration value="sponge"/>
 *     &lt;enumeration value="glass"/>
 *     &lt;enumeration value="lapis_ore"/>
 *     &lt;enumeration value="lapis_block"/>
 *     &lt;enumeration value="dispenser"/>
 *     &lt;enumeration value="sandstone"/>
 *     &lt;enumeration value="noteblock"/>
 *     &lt;enumeration value="bed"/>
 *     &lt;enumeration value="golden_rail"/>
 *     &lt;enumeration value="detector_rail"/>
 *     &lt;enumeration value="sticky_piston"/>
 *     &lt;enumeration value="web"/>
 *     &lt;enumeration value="tallgrass"/>
 *     &lt;enumeration value="deadbush"/>
 *     &lt;enumeration value="piston"/>
 *     &lt;enumeration value="piston_head"/>
 *     &lt;enumeration value="wool"/>
 *     &lt;enumeration value="piston_extension"/>
 *     &lt;enumeration value="yellow_flower"/>
 *     &lt;enumeration value="red_flower"/>
 *     &lt;enumeration value="brown_mushroom"/>
 *     &lt;enumeration value="red_mushroom"/>
 *     &lt;enumeration value="gold_block"/>
 *     &lt;enumeration value="iron_block"/>
 *     &lt;enumeration value="double_stone_slab"/>
 *     &lt;enumeration value="stone_slab"/>
 *     &lt;enumeration value="brick_block"/>
 *     &lt;enumeration value="tnt"/>
 *     &lt;enumeration value="bookshelf"/>
 *     &lt;enumeration value="mossy_cobblestone"/>
 *     &lt;enumeration value="obsidian"/>
 *     &lt;enumeration value="torch"/>
 *     &lt;enumeration value="fire"/>
 *     &lt;enumeration value="mob_spawner"/>
 *     &lt;enumeration value="oak_stairs"/>
 *     &lt;enumeration value="chest"/>
 *     &lt;enumeration value="redstone_wire"/>
 *     &lt;enumeration value="diamond_ore"/>
 *     &lt;enumeration value="diamond_block"/>
 *     &lt;enumeration value="crafting_table"/>
 *     &lt;enumeration value="wheat"/>
 *     &lt;enumeration value="farmland"/>
 *     &lt;enumeration value="furnace"/>
 *     &lt;enumeration value="lit_furnace"/>
 *     &lt;enumeration value="standing_sign"/>
 *     &lt;enumeration value="wooden_door"/>
 *     &lt;enumeration value="ladder"/>
 *     &lt;enumeration value="rail"/>
 *     &lt;enumeration value="stone_stairs"/>
 *     &lt;enumeration value="wall_sign"/>
 *     &lt;enumeration value="lever"/>
 *     &lt;enumeration value="stone_pressure_plate"/>
 *     &lt;enumeration value="iron_door"/>
 *     &lt;enumeration value="wooden_pressure_plate"/>
 *     &lt;enumeration value="redstone_ore"/>
 *     &lt;enumeration value="lit_redstone_ore"/>
 *     &lt;enumeration value="unlit_redstone_torch"/>
 *     &lt;enumeration value="redstone_torch"/>
 *     &lt;enumeration value="stone_button"/>
 *     &lt;enumeration value="snow_layer"/>
 *     &lt;enumeration value="ice"/>
 *     &lt;enumeration value="snow"/>
 *     &lt;enumeration value="cactus"/>
 *     &lt;enumeration value="clay"/>
 *     &lt;enumeration value="reeds"/>
 *     &lt;enumeration value="jukebox"/>
 *     &lt;enumeration value="fence"/>
 *     &lt;enumeration value="pumpkin"/>
 *     &lt;enumeration value="netherrack"/>
 *     &lt;enumeration value="soul_sand"/>
 *     &lt;enumeration value="glowstone"/>
 *     &lt;enumeration value="portal"/>
 *     &lt;enumeration value="lit_pumpkin"/>
 *     &lt;enumeration value="cake"/>
 *     &lt;enumeration value="unpowered_repeater"/>
 *     &lt;enumeration value="powered_repeater"/>
 *     &lt;enumeration value="stained_glass"/>
 *     &lt;enumeration value="trapdoor"/>
 *     &lt;enumeration value="monster_egg"/>
 *     &lt;enumeration value="stonebrick"/>
 *     &lt;enumeration value="brown_mushroom_block"/>
 *     &lt;enumeration value="red_mushroom_block"/>
 *     &lt;enumeration value="iron_bars"/>
 *     &lt;enumeration value="glass_pane"/>
 *     &lt;enumeration value="melon_block"/>
 *     &lt;enumeration value="pumpkin_stem"/>
 *     &lt;enumeration value="melon_stem"/>
 *     &lt;enumeration value="vine"/>
 *     &lt;enumeration value="fence_gate"/>
 *     &lt;enumeration value="brick_stairs"/>
 *     &lt;enumeration value="stone_brick_stairs"/>
 *     &lt;enumeration value="mycelium"/>
 *     &lt;enumeration value="waterlily"/>
 *     &lt;enumeration value="nether_brick"/>
 *     &lt;enumeration value="nether_brick_fence"/>
 *     &lt;enumeration value="nether_brick_stairs"/>
 *     &lt;enumeration value="nether_wart"/>
 *     &lt;enumeration value="enchanting_table"/>
 *     &lt;enumeration value="brewing_stand"/>
 *     &lt;enumeration value="cauldron"/>
 *     &lt;enumeration value="end_portal"/>
 *     &lt;enumeration value="end_portal_frame"/>
 *     &lt;enumeration value="end_stone"/>
 *     &lt;enumeration value="dragon_egg"/>
 *     &lt;enumeration value="redstone_lamp"/>
 *     &lt;enumeration value="lit_redstone_lamp"/>
 *     &lt;enumeration value="double_wooden_slab"/>
 *     &lt;enumeration value="wooden_slab"/>
 *     &lt;enumeration value="cocoa"/>
 *     &lt;enumeration value="sandstone_stairs"/>
 *     &lt;enumeration value="emerald_ore"/>
 *     &lt;enumeration value="ender_chest"/>
 *     &lt;enumeration value="tripwire_hook"/>
 *     &lt;enumeration value="tripwire"/>
 *     &lt;enumeration value="emerald_block"/>
 *     &lt;enumeration value="spruce_stairs"/>
 *     &lt;enumeration value="birch_stairs"/>
 *     &lt;enumeration value="jungle_stairs"/>
 *     &lt;enumeration value="command_block"/>
 *     &lt;enumeration value="beacon"/>
 *     &lt;enumeration value="cobblestone_wall"/>
 *     &lt;enumeration value="flower_pot"/>
 *     &lt;enumeration value="carrots"/>
 *     &lt;enumeration value="potatoes"/>
 *     &lt;enumeration value="wooden_button"/>
 *     &lt;enumeration value="skull"/>
 *     &lt;enumeration value="anvil"/>
 *     &lt;enumeration value="trapped_chest"/>
 *     &lt;enumeration value="light_weighted_pressure_plate"/>
 *     &lt;enumeration value="heavy_weighted_pressure_plate"/>
 *     &lt;enumeration value="unpowered_comparator"/>
 *     &lt;enumeration value="powered_comparator"/>
 *     &lt;enumeration value="daylight_detector"/>
 *     &lt;enumeration value="redstone_block"/>
 *     &lt;enumeration value="quartz_ore"/>
 *     &lt;enumeration value="hopper"/>
 *     &lt;enumeration value="quartz_block"/>
 *     &lt;enumeration value="quartz_stairs"/>
 *     &lt;enumeration value="activator_rail"/>
 *     &lt;enumeration value="dropper"/>
 *     &lt;enumeration value="stained_hardened_clay"/>
 *     &lt;enumeration value="stained_glass_pane"/>
 *     &lt;enumeration value="leaves2"/>
 *     &lt;enumeration value="log2"/>
 *     &lt;enumeration value="acacia_stairs"/>
 *     &lt;enumeration value="dark_oak_stairs"/>
 *     &lt;enumeration value="slime"/>
 *     &lt;enumeration value="barrier"/>
 *     &lt;enumeration value="iron_trapdoor"/>
 *     &lt;enumeration value="prismarine"/>
 *     &lt;enumeration value="sea_lantern"/>
 *     &lt;enumeration value="hay_block"/>
 *     &lt;enumeration value="carpet"/>
 *     &lt;enumeration value="hardened_clay"/>
 *     &lt;enumeration value="coal_block"/>
 *     &lt;enumeration value="packed_ice"/>
 *     &lt;enumeration value="double_plant"/>
 *     &lt;enumeration value="standing_banner"/>
 *     &lt;enumeration value="wall_banner"/>
 *     &lt;enumeration value="daylight_detector_inverted"/>
 *     &lt;enumeration value="red_sandstone"/>
 *     &lt;enumeration value="red_sandstone_stairs"/>
 *     &lt;enumeration value="double_stone_slab2"/>
 *     &lt;enumeration value="stone_slab2"/>
 *     &lt;enumeration value="spruce_fence_gate"/>
 *     &lt;enumeration value="birch_fence_gate"/>
 *     &lt;enumeration value="jungle_fence_gate"/>
 *     &lt;enumeration value="dark_oak_fence_gate"/>
 *     &lt;enumeration value="acacia_fence_gate"/>
 *     &lt;enumeration value="spruce_fence"/>
 *     &lt;enumeration value="birch_fence"/>
 *     &lt;enumeration value="jungle_fence"/>
 *     &lt;enumeration value="dark_oak_fence"/>
 *     &lt;enumeration value="acacia_fence"/>
 *     &lt;enumeration value="spruce_door"/>
 *     &lt;enumeration value="birch_door"/>
 *     &lt;enumeration value="jungle_door"/>
 *     &lt;enumeration value="acacia_door"/>
 *     &lt;enumeration value="dark_oak_door"/>
 *     &lt;enumeration value="end_rod"/>
 *     &lt;enumeration value="chorus_plant"/>
 *     &lt;enumeration value="chorus_flower"/>
 *     &lt;enumeration value="purpur_block"/>
 *     &lt;enumeration value="purpur_pillar"/>
 *     &lt;enumeration value="purpur_stairs"/>
 *     &lt;enumeration value="purpur_double_slab"/>
 *     &lt;enumeration value="purpur_slab"/>
 *     &lt;enumeration value="end_bricks"/>
 *     &lt;enumeration value="beetroots"/>
 *     &lt;enumeration value="grass_path"/>
 *     &lt;enumeration value="end_gateway"/>
 *     &lt;enumeration value="repeating_command_block"/>
 *     &lt;enumeration value="chain_command_block"/>
 *     &lt;enumeration value="frosted_ice"/>
 *     &lt;enumeration value="magma"/>
 *     &lt;enumeration value="nether_wart_block"/>
 *     &lt;enumeration value="red_nether_brick"/>
 *     &lt;enumeration value="bone_block"/>
 *     &lt;enumeration value="structure_void"/>
 *     &lt;enumeration value="observer"/>
 *     &lt;enumeration value="white_shulker_box"/>
 *     &lt;enumeration value="orange_shulker_box"/>
 *     &lt;enumeration value="magenta_shulker_box"/>
 *     &lt;enumeration value="light_blue_shulker_box"/>
 *     &lt;enumeration value="yellow_shulker_box"/>
 *     &lt;enumeration value="lime_shulker_box"/>
 *     &lt;enumeration value="pink_shulker_box"/>
 *     &lt;enumeration value="gray_shulker_box"/>
 *     &lt;enumeration value="silver_shulker_box"/>
 *     &lt;enumeration value="cyan_shulker_box"/>
 *     &lt;enumeration value="purple_shulker_box"/>
 *     &lt;enumeration value="blue_shulker_box"/>
 *     &lt;enumeration value="brown_shulker_box"/>
 *     &lt;enumeration value="green_shulker_box"/>
 *     &lt;enumeration value="red_shulker_box"/>
 *     &lt;enumeration value="black_shulker_box"/>
 *     &lt;enumeration value="structure_block"/>
 *   &lt;/restriction>
 * &lt;/simpleType>
 * </pre>
 * 
 */
@XmlType(name = "BlockType")
@XmlEnum
public enum BlockType {

    @XmlEnumValue("air")
    AIR("air"),
    @XmlEnumValue("stone")
    STONE("stone"),
    @XmlEnumValue("grass")
    GRASS("grass"),
    @XmlEnumValue("dirt")
    DIRT("dirt"),
    @XmlEnumValue("cobblestone")
    COBBLESTONE("cobblestone"),
    @XmlEnumValue("planks")
    PLANKS("planks"),
    @XmlEnumValue("sapling")
    SAPLING("sapling"),
    @XmlEnumValue("bedrock")
    BEDROCK("bedrock"),
    @XmlEnumValue("flowing_water")
    FLOWING_WATER("flowing_water"),
    @XmlEnumValue("water")
    WATER("water"),
    @XmlEnumValue("flowing_lava")
    FLOWING_LAVA("flowing_lava"),
    @XmlEnumValue("lava")
    LAVA("lava"),
    @XmlEnumValue("sand")
    SAND("sand"),
    @XmlEnumValue("gravel")
    GRAVEL("gravel"),
    @XmlEnumValue("gold_ore")
    GOLD_ORE("gold_ore"),
    @XmlEnumValue("iron_ore")
    IRON_ORE("iron_ore"),
    @XmlEnumValue("coal_ore")
    COAL_ORE("coal_ore"),
    @XmlEnumValue("log")
    LOG("log"),
    @XmlEnumValue("leaves")
    LEAVES("leaves"),
    @XmlEnumValue("sponge")
    SPONGE("sponge"),
    @XmlEnumValue("glass")
    GLASS("glass"),
    @XmlEnumValue("lapis_ore")
    LAPIS_ORE("lapis_ore"),
    @XmlEnumValue("lapis_block")
    LAPIS_BLOCK("lapis_block"),
    @XmlEnumValue("dispenser")
    DISPENSER("dispenser"),
    @XmlEnumValue("sandstone")
    SANDSTONE("sandstone"),
    @XmlEnumValue("noteblock")
    NOTEBLOCK("noteblock"),
    @XmlEnumValue("bed")
    BED("bed"),
    @XmlEnumValue("golden_rail")
    GOLDEN_RAIL("golden_rail"),
    @XmlEnumValue("detector_rail")
    DETECTOR_RAIL("detector_rail"),
    @XmlEnumValue("sticky_piston")
    STICKY_PISTON("sticky_piston"),
    @XmlEnumValue("web")
    WEB("web"),
    @XmlEnumValue("tallgrass")
    TALLGRASS("tallgrass"),
    @XmlEnumValue("deadbush")
    DEADBUSH("deadbush"),
    @XmlEnumValue("piston")
    PISTON("piston"),
    @XmlEnumValue("piston_head")
    PISTON_HEAD("piston_head"),
    @XmlEnumValue("wool")
    WOOL("wool"),
    @XmlEnumValue("piston_extension")
    PISTON_EXTENSION("piston_extension"),
    @XmlEnumValue("yellow_flower")
    YELLOW_FLOWER("yellow_flower"),
    @XmlEnumValue("red_flower")
    RED_FLOWER("red_flower"),
    @XmlEnumValue("brown_mushroom")
    BROWN_MUSHROOM("brown_mushroom"),
    @XmlEnumValue("red_mushroom")
    RED_MUSHROOM("red_mushroom"),
    @XmlEnumValue("gold_block")
    GOLD_BLOCK("gold_block"),
    @XmlEnumValue("iron_block")
    IRON_BLOCK("iron_block"),
    @XmlEnumValue("double_stone_slab")
    DOUBLE_STONE_SLAB("double_stone_slab"),
    @XmlEnumValue("stone_slab")
    STONE_SLAB("stone_slab"),
    @XmlEnumValue("brick_block")
    BRICK_BLOCK("brick_block"),
    @XmlEnumValue("tnt")
    TNT("tnt"),
    @XmlEnumValue("bookshelf")
    BOOKSHELF("bookshelf"),
    @XmlEnumValue("mossy_cobblestone")
    MOSSY_COBBLESTONE("mossy_cobblestone"),
    @XmlEnumValue("obsidian")
    OBSIDIAN("obsidian"),
    @XmlEnumValue("torch")
    TORCH("torch"),
    @XmlEnumValue("fire")
    FIRE("fire"),
    @XmlEnumValue("mob_spawner")
    MOB_SPAWNER("mob_spawner"),
    @XmlEnumValue("oak_stairs")
    OAK_STAIRS("oak_stairs"),
    @XmlEnumValue("chest")
    CHEST("chest"),
    @XmlEnumValue("redstone_wire")
    REDSTONE_WIRE("redstone_wire"),
    @XmlEnumValue("diamond_ore")
    DIAMOND_ORE("diamond_ore"),
    @XmlEnumValue("diamond_block")
    DIAMOND_BLOCK("diamond_block"),
    @XmlEnumValue("crafting_table")
    CRAFTING_TABLE("crafting_table"),
    @XmlEnumValue("wheat")
    WHEAT("wheat"),
    @XmlEnumValue("farmland")
    FARMLAND("farmland"),
    @XmlEnumValue("furnace")
    FURNACE("furnace"),
    @XmlEnumValue("lit_furnace")
    LIT_FURNACE("lit_furnace"),
    @XmlEnumValue("standing_sign")
    STANDING_SIGN("standing_sign"),
    @XmlEnumValue("wooden_door")
    WOODEN_DOOR("wooden_door"),
    @XmlEnumValue("ladder")
    LADDER("ladder"),
    @XmlEnumValue("rail")
    RAIL("rail"),
    @XmlEnumValue("stone_stairs")
    STONE_STAIRS("stone_stairs"),
    @XmlEnumValue("wall_sign")
    WALL_SIGN("wall_sign"),
    @XmlEnumValue("lever")
    LEVER("lever"),
    @XmlEnumValue("stone_pressure_plate")
    STONE_PRESSURE_PLATE("stone_pressure_plate"),
    @XmlEnumValue("iron_door")
    IRON_DOOR("iron_door"),
    @XmlEnumValue("wooden_pressure_plate")
    WOODEN_PRESSURE_PLATE("wooden_pressure_plate"),
    @XmlEnumValue("redstone_ore")
    REDSTONE_ORE("redstone_ore"),
    @XmlEnumValue("lit_redstone_ore")
    LIT_REDSTONE_ORE("lit_redstone_ore"),
    @XmlEnumValue("unlit_redstone_torch")
    UNLIT_REDSTONE_TORCH("unlit_redstone_torch"),
    @XmlEnumValue("redstone_torch")
    REDSTONE_TORCH("redstone_torch"),
    @XmlEnumValue("stone_button")
    STONE_BUTTON("stone_button"),
    @XmlEnumValue("snow_layer")
    SNOW_LAYER("snow_layer"),
    @XmlEnumValue("ice")
    ICE("ice"),
    @XmlEnumValue("snow")
    SNOW("snow"),
    @XmlEnumValue("cactus")
    CACTUS("cactus"),
    @XmlEnumValue("clay")
    CLAY("clay"),
    @XmlEnumValue("reeds")
    REEDS("reeds"),
    @XmlEnumValue("jukebox")
    JUKEBOX("jukebox"),
    @XmlEnumValue("fence")
    FENCE("fence"),
    @XmlEnumValue("pumpkin")
    PUMPKIN("pumpkin"),
    @XmlEnumValue("netherrack")
    NETHERRACK("netherrack"),
    @XmlEnumValue("soul_sand")
    SOUL_SAND("soul_sand"),
    @XmlEnumValue("glowstone")
    GLOWSTONE("glowstone"),
    @XmlEnumValue("portal")
    PORTAL("portal"),
    @XmlEnumValue("lit_pumpkin")
    LIT_PUMPKIN("lit_pumpkin"),
    @XmlEnumValue("cake")
    CAKE("cake"),
    @XmlEnumValue("unpowered_repeater")
    UNPOWERED_REPEATER("unpowered_repeater"),
    @XmlEnumValue("powered_repeater")
    POWERED_REPEATER("powered_repeater"),
    @XmlEnumValue("stained_glass")
    STAINED_GLASS("stained_glass"),
    @XmlEnumValue("trapdoor")
    TRAPDOOR("trapdoor"),
    @XmlEnumValue("monster_egg")
    MONSTER_EGG("monster_egg"),
    @XmlEnumValue("stonebrick")
    STONEBRICK("stonebrick"),
    @XmlEnumValue("brown_mushroom_block")
    BROWN_MUSHROOM_BLOCK("brown_mushroom_block"),
    @XmlEnumValue("red_mushroom_block")
    RED_MUSHROOM_BLOCK("red_mushroom_block"),
    @XmlEnumValue("iron_bars")
    IRON_BARS("iron_bars"),
    @XmlEnumValue("glass_pane")
    GLASS_PANE("glass_pane"),
    @XmlEnumValue("melon_block")
    MELON_BLOCK("melon_block"),
    @XmlEnumValue("pumpkin_stem")
    PUMPKIN_STEM("pumpkin_stem"),
    @XmlEnumValue("melon_stem")
    MELON_STEM("melon_stem"),
    @XmlEnumValue("vine")
    VINE("vine"),
    @XmlEnumValue("fence_gate")
    FENCE_GATE("fence_gate"),
    @XmlEnumValue("brick_stairs")
    BRICK_STAIRS("brick_stairs"),
    @XmlEnumValue("stone_brick_stairs")
    STONE_BRICK_STAIRS("stone_brick_stairs"),
    @XmlEnumValue("mycelium")
    MYCELIUM("mycelium"),
    @XmlEnumValue("waterlily")
    WATERLILY("waterlily"),
    @XmlEnumValue("nether_brick")
    NETHER_BRICK("nether_brick"),
    @XmlEnumValue("nether_brick_fence")
    NETHER_BRICK_FENCE("nether_brick_fence"),
    @XmlEnumValue("nether_brick_stairs")
    NETHER_BRICK_STAIRS("nether_brick_stairs"),
    @XmlEnumValue("nether_wart")
    NETHER_WART("nether_wart"),
    @XmlEnumValue("enchanting_table")
    ENCHANTING_TABLE("enchanting_table"),
    @XmlEnumValue("brewing_stand")
    BREWING_STAND("brewing_stand"),
    @XmlEnumValue("cauldron")
    CAULDRON("cauldron"),
    @XmlEnumValue("end_portal")
    END_PORTAL("end_portal"),
    @XmlEnumValue("end_portal_frame")
    END_PORTAL_FRAME("end_portal_frame"),
    @XmlEnumValue("end_stone")
    END_STONE("end_stone"),
    @XmlEnumValue("dragon_egg")
    DRAGON_EGG("dragon_egg"),
    @XmlEnumValue("redstone_lamp")
    REDSTONE_LAMP("redstone_lamp"),
    @XmlEnumValue("lit_redstone_lamp")
    LIT_REDSTONE_LAMP("lit_redstone_lamp"),
    @XmlEnumValue("double_wooden_slab")
    DOUBLE_WOODEN_SLAB("double_wooden_slab"),
    @XmlEnumValue("wooden_slab")
    WOODEN_SLAB("wooden_slab"),
    @XmlEnumValue("cocoa")
    COCOA("cocoa"),
    @XmlEnumValue("sandstone_stairs")
    SANDSTONE_STAIRS("sandstone_stairs"),
    @XmlEnumValue("emerald_ore")
    EMERALD_ORE("emerald_ore"),
    @XmlEnumValue("ender_chest")
    ENDER_CHEST("ender_chest"),
    @XmlEnumValue("tripwire_hook")
    TRIPWIRE_HOOK("tripwire_hook"),
    @XmlEnumValue("tripwire")
    TRIPWIRE("tripwire"),
    @XmlEnumValue("emerald_block")
    EMERALD_BLOCK("emerald_block"),
    @XmlEnumValue("spruce_stairs")
    SPRUCE_STAIRS("spruce_stairs"),
    @XmlEnumValue("birch_stairs")
    BIRCH_STAIRS("birch_stairs"),
    @XmlEnumValue("jungle_stairs")
    JUNGLE_STAIRS("jungle_stairs"),
    @XmlEnumValue("command_block")
    COMMAND_BLOCK("command_block"),
    @XmlEnumValue("beacon")
    BEACON("beacon"),
    @XmlEnumValue("cobblestone_wall")
    COBBLESTONE_WALL("cobblestone_wall"),
    @XmlEnumValue("flower_pot")
    FLOWER_POT("flower_pot"),
    @XmlEnumValue("carrots")
    CARROTS("carrots"),
    @XmlEnumValue("potatoes")
    POTATOES("potatoes"),
    @XmlEnumValue("wooden_button")
    WOODEN_BUTTON("wooden_button"),
    @XmlEnumValue("skull")
    SKULL("skull"),
    @XmlEnumValue("anvil")
    ANVIL("anvil"),
    @XmlEnumValue("trapped_chest")
    TRAPPED_CHEST("trapped_chest"),
    @XmlEnumValue("light_weighted_pressure_plate")
    LIGHT_WEIGHTED_PRESSURE_PLATE("light_weighted_pressure_plate"),
    @XmlEnumValue("heavy_weighted_pressure_plate")
    HEAVY_WEIGHTED_PRESSURE_PLATE("heavy_weighted_pressure_plate"),
    @XmlEnumValue("unpowered_comparator")
    UNPOWERED_COMPARATOR("unpowered_comparator"),
    @XmlEnumValue("powered_comparator")
    POWERED_COMPARATOR("powered_comparator"),
    @XmlEnumValue("daylight_detector")
    DAYLIGHT_DETECTOR("daylight_detector"),
    @XmlEnumValue("redstone_block")
    REDSTONE_BLOCK("redstone_block"),
    @XmlEnumValue("quartz_ore")
    QUARTZ_ORE("quartz_ore"),
    @XmlEnumValue("hopper")
    HOPPER("hopper"),
    @XmlEnumValue("quartz_block")
    QUARTZ_BLOCK("quartz_block"),
    @XmlEnumValue("quartz_stairs")
    QUARTZ_STAIRS("quartz_stairs"),
    @XmlEnumValue("activator_rail")
    ACTIVATOR_RAIL("activator_rail"),
    @XmlEnumValue("dropper")
    DROPPER("dropper"),
    @XmlEnumValue("stained_hardened_clay")
    STAINED_HARDENED_CLAY("stained_hardened_clay"),
    @XmlEnumValue("stained_glass_pane")
    STAINED_GLASS_PANE("stained_glass_pane"),
    @XmlEnumValue("leaves2")
    LEAVES_2("leaves2"),
    @XmlEnumValue("log2")
    LOG_2("log2"),
    @XmlEnumValue("acacia_stairs")
    ACACIA_STAIRS("acacia_stairs"),
    @XmlEnumValue("dark_oak_stairs")
    DARK_OAK_STAIRS("dark_oak_stairs"),
    @XmlEnumValue("slime")
    SLIME("slime"),
    @XmlEnumValue("barrier")
    BARRIER("barrier"),
    @XmlEnumValue("iron_trapdoor")
    IRON_TRAPDOOR("iron_trapdoor"),
    @XmlEnumValue("prismarine")
    PRISMARINE("prismarine"),
    @XmlEnumValue("sea_lantern")
    SEA_LANTERN("sea_lantern"),
    @XmlEnumValue("hay_block")
    HAY_BLOCK("hay_block"),
    @XmlEnumValue("carpet")
    CARPET("carpet"),
    @XmlEnumValue("hardened_clay")
    HARDENED_CLAY("hardened_clay"),
    @XmlEnumValue("coal_block")
    COAL_BLOCK("coal_block"),
    @XmlEnumValue("packed_ice")
    PACKED_ICE("packed_ice"),
    @XmlEnumValue("double_plant")
    DOUBLE_PLANT("double_plant"),
    @XmlEnumValue("standing_banner")
    STANDING_BANNER("standing_banner"),
    @XmlEnumValue("wall_banner")
    WALL_BANNER("wall_banner"),
    @XmlEnumValue("daylight_detector_inverted")
    DAYLIGHT_DETECTOR_INVERTED("daylight_detector_inverted"),
    @XmlEnumValue("red_sandstone")
    RED_SANDSTONE("red_sandstone"),
    @XmlEnumValue("red_sandstone_stairs")
    RED_SANDSTONE_STAIRS("red_sandstone_stairs"),
    @XmlEnumValue("double_stone_slab2")
    DOUBLE_STONE_SLAB_2("double_stone_slab2"),
    @XmlEnumValue("stone_slab2")
    STONE_SLAB_2("stone_slab2"),
    @XmlEnumValue("spruce_fence_gate")
    SPRUCE_FENCE_GATE("spruce_fence_gate"),
    @XmlEnumValue("birch_fence_gate")
    BIRCH_FENCE_GATE("birch_fence_gate"),
    @XmlEnumValue("jungle_fence_gate")
    JUNGLE_FENCE_GATE("jungle_fence_gate"),
    @XmlEnumValue("dark_oak_fence_gate")
    DARK_OAK_FENCE_GATE("dark_oak_fence_gate"),
    @XmlEnumValue("acacia_fence_gate")
    ACACIA_FENCE_GATE("acacia_fence_gate"),
    @XmlEnumValue("spruce_fence")
    SPRUCE_FENCE("spruce_fence"),
    @XmlEnumValue("birch_fence")
    BIRCH_FENCE("birch_fence"),
    @XmlEnumValue("jungle_fence")
    JUNGLE_FENCE("jungle_fence"),
    @XmlEnumValue("dark_oak_fence")
    DARK_OAK_FENCE("dark_oak_fence"),
    @XmlEnumValue("acacia_fence")
    ACACIA_FENCE("acacia_fence"),
    @XmlEnumValue("spruce_door")
    SPRUCE_DOOR("spruce_door"),
    @XmlEnumValue("birch_door")
    BIRCH_DOOR("birch_door"),
    @XmlEnumValue("jungle_door")
    JUNGLE_DOOR("jungle_door"),
    @XmlEnumValue("acacia_door")
    ACACIA_DOOR("acacia_door"),
    @XmlEnumValue("dark_oak_door")
    DARK_OAK_DOOR("dark_oak_door"),
    @XmlEnumValue("end_rod")
    END_ROD("end_rod"),
    @XmlEnumValue("chorus_plant")
    CHORUS_PLANT("chorus_plant"),
    @XmlEnumValue("chorus_flower")
    CHORUS_FLOWER("chorus_flower"),
    @XmlEnumValue("purpur_block")
    PURPUR_BLOCK("purpur_block"),
    @XmlEnumValue("purpur_pillar")
    PURPUR_PILLAR("purpur_pillar"),
    @XmlEnumValue("purpur_stairs")
    PURPUR_STAIRS("purpur_stairs"),
    @XmlEnumValue("purpur_double_slab")
    PURPUR_DOUBLE_SLAB("purpur_double_slab"),
    @XmlEnumValue("purpur_slab")
    PURPUR_SLAB("purpur_slab"),
    @XmlEnumValue("end_bricks")
    END_BRICKS("end_bricks"),
    @XmlEnumValue("beetroots")
    BEETROOTS("beetroots"),
    @XmlEnumValue("grass_path")
    GRASS_PATH("grass_path"),
    @XmlEnumValue("end_gateway")
    END_GATEWAY("end_gateway"),
    @XmlEnumValue("repeating_command_block")
    REPEATING_COMMAND_BLOCK("repeating_command_block"),
    @XmlEnumValue("chain_command_block")
    CHAIN_COMMAND_BLOCK("chain_command_block"),
    @XmlEnumValue("frosted_ice")
    FROSTED_ICE("frosted_ice"),
    @XmlEnumValue("magma")
    MAGMA("magma"),
    @XmlEnumValue("nether_wart_block")
    NETHER_WART_BLOCK("nether_wart_block"),
    @XmlEnumValue("red_nether_brick")
    RED_NETHER_BRICK("red_nether_brick"),
    @XmlEnumValue("bone_block")
    BONE_BLOCK("bone_block"),
    @XmlEnumValue("structure_void")
    STRUCTURE_VOID("structure_void"),
    @XmlEnumValue("observer")
    OBSERVER("observer"),
    @XmlEnumValue("white_shulker_box")
    WHITE_SHULKER_BOX("white_shulker_box"),
    @XmlEnumValue("orange_shulker_box")
    ORANGE_SHULKER_BOX("orange_shulker_box"),
    @XmlEnumValue("magenta_shulker_box")
    MAGENTA_SHULKER_BOX("magenta_shulker_box"),
    @XmlEnumValue("light_blue_shulker_box")
    LIGHT_BLUE_SHULKER_BOX("light_blue_shulker_box"),
    @XmlEnumValue("yellow_shulker_box")
    YELLOW_SHULKER_BOX("yellow_shulker_box"),
    @XmlEnumValue("lime_shulker_box")
    LIME_SHULKER_BOX("lime_shulker_box"),
    @XmlEnumValue("pink_shulker_box")
    PINK_SHULKER_BOX("pink_shulker_box"),
    @XmlEnumValue("gray_shulker_box")
    GRAY_SHULKER_BOX("gray_shulker_box"),
    @XmlEnumValue("silver_shulker_box")
    SILVER_SHULKER_BOX("silver_shulker_box"),
    @XmlEnumValue("cyan_shulker_box")
    CYAN_SHULKER_BOX("cyan_shulker_box"),
    @XmlEnumValue("purple_shulker_box")
    PURPLE_SHULKER_BOX("purple_shulker_box"),
    @XmlEnumValue("blue_shulker_box")
    BLUE_SHULKER_BOX("blue_shulker_box"),
    @XmlEnumValue("brown_shulker_box")
    BROWN_SHULKER_BOX("brown_shulker_box"),
    @XmlEnumValue("green_shulker_box")
    GREEN_SHULKER_BOX("green_shulker_box"),
    @XmlEnumValue("red_shulker_box")
    RED_SHULKER_BOX("red_shulker_box"),
    @XmlEnumValue("black_shulker_box")
    BLACK_SHULKER_BOX("black_shulker_box"),
    @XmlEnumValue("structure_block")
    STRUCTURE_BLOCK("structure_block");
    private final String value;

    BlockType(String v) {
        value = v;
    }

    public String value() {
        return value;
    }

    public static BlockType fromValue(String v) {
        for (BlockType c: BlockType.values()) {
            if (c.value.equals(v)) {
                return c;
            }
        }
        throw new IllegalArgumentException(v);
    }

}
