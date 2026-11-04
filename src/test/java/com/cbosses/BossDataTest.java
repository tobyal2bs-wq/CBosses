package com.cbosses;

import com.cbosses.fight.BossDef;
import com.cbosses.fight.BossService;
import com.cbosses.model.ModelRig;
import com.cbosses.season.Seasons;
import org.bukkit.configuration.file.YamlConfiguration;
import org.junit.jupiter.api.Test;

import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.MonthDay;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.util.List;
import java.util.Map;
import java.util.logging.Logger;

import static org.junit.jupiter.api.Assertions.*;

class BossDataTest {

    private static Map<String, ModelRig.Model> models() throws Exception {
        try (var in = BossDataTest.class.getResourceAsStream("/models.json")) {
            assertNotNull(in, "models.json is missing");
            return ModelRig.load(new InputStreamReader(in, StandardCharsets.UTF_8));
        }
    }

    private static Map<String, BossDef> bosses() throws Exception {
        try (var in = BossDataTest.class.getResourceAsStream("/bosses.yml")) {
            assertNotNull(in, "bosses.yml is missing");
            YamlConfiguration yaml = YamlConfiguration.loadConfiguration(new InputStreamReader(in, StandardCharsets.UTF_8));
            int listed = yaml.getConfigurationSection("bosses").getKeys(false).size();
            Map<String, BossDef> defs = BossDef.load(yaml, Logger.getLogger("test"));
            assertEquals(listed, defs.size(), "every boss in bosses.yml loads");
            return defs;
        }
    }

    @Test
    void everyBossHasAModelWithAnEntranceAndADeath() throws Exception {
        var models = models();
        var defs = bosses();
        assertTrue(defs.size() >= 42, "42 bosses or more");
        for (BossDef d : defs.values()) {
            ModelRig.Model m = models.get(d.model());
            assertNotNull(m, d.id() + " has no model");
            assertFalse(m.spawn.isEmpty(), d.id() + " has no entrance");
            assertFalse(m.death.isEmpty(), d.id() + " has no death");
            for (var s : m.spawn) assertTrue(ModelRig.OPS.contains(s.op()) || s.op().equals("fx"), d.id() + " entrance step " + s.op());
            for (var s : m.death) assertTrue(ModelRig.OPS.contains(s.op()) || s.op().equals("fx"), d.id() + " death step " + s.op());
            assertTrue(m.death.stream().anyMatch(s -> s.op().equals("flash")), d.id() + " death has no flash");
            for (String anim : m.attackAnimations()) assertNotNull(m.anim(anim), d.id() + " attack animation " + anim + " is not in rig " + m.rig);
            assertNotNull(m.anim("idle"), d.id() + " idle");
            assertNotNull(m.anim("hurt"), d.id() + " hurt");
            if (d.flies()) assertNotNull(m.anim("idle"), d.id() + " flies");
        }
    }

    @Test
    void everyModelHasAtLeast120BlocksAndCanDropItsDetail() throws Exception {
        var full = models();
        for (var e : full.entrySet()) assertTrue(e.getValue().cubes.size() >= 120, e.getKey() + " has only " + e.getValue().cubes.size() + " blocks");
        int was = ModelRig.detail;
        try {
            ModelRig.detail = 0;
            var low = models();
            for (var e : low.entrySet()) {
                assertTrue(low.get(e.getKey()).cubes.size() < full.get(e.getKey()).cubes.size(), e.getKey() + " keeps every block on low detail");
                assertFalse(low.get(e.getKey()).cubes.isEmpty(), e.getKey() + " is empty on low detail");
            }
        } finally { ModelRig.detail = was; }
    }

    @Test
    void theFinaleBossExistsAndIsKeptOutOfTheWeeklyRotation() throws Exception {
        var defs = bosses();
        assertNotNull(defs.get("the_unmaker"), "the finale boss");
        for (String legend : new String[]{"withered_tyrant", "ender_wyrm", "the_listener"}) assertNotNull(defs.get(legend), legend);
        ModelRig.Model m = models().get("the_unmaker");
        assertTrue(m.cubes.size() >= 200, "the finale is the most detailed boss");
        assertTrue(m.death.stream().anyMatch(s -> s.op().equals("shatter")), "the finale shatters");
    }

    @Test
    void chapterBossesCoverTenChapters() throws Exception {
        var defs = bosses();
        for (int ch = 1; ch <= 10; ch++) {
            int n = ch;
            assertTrue(defs.values().stream().anyMatch(d -> d.chapterBoss() && d.chapter() == n), "no boss for chapter " + ch);
        }
    }

    @Test
    void cluckworthHatchesFromAnEggThatOnlyShowsDuringItsEntrance() throws Exception {
        ModelRig.Model m = models().get("clucksworth");
        int shell = 0;
        for (boolean b : m.entranceOnly) if (b) shell++;
        assertTrue(shell >= 10, "the egg has pieces");
        assertTrue(m.spawn.stream().anyMatch(s -> s.op().equals("shatter")), "the egg shatters");
    }

    @Test
    void scheduleFindsTheNextSlot() {
        ZonedDateTime now = ZonedDateTime.of(2026, 11, 4, 12, 0, 0, 0, ZoneOffset.UTC); // a Wednesday
        ZonedDateTime next = BossService.nextAfter(now, List.of(DayOfWeek.SATURDAY), LocalTime.of(20, 0), "");
        assertEquals(LocalDate.of(2026, 11, 7), next.toLocalDate());
        ZonedDateTime skip = BossService.nextAfter(now, List.of(DayOfWeek.SATURDAY), LocalTime.of(20, 0), "2026-11-07 20:00");
        assertEquals(LocalDate.of(2026, 11, 14), skip.toLocalDate());
    }

    @Test
    void seasonsWrapAroundNewYear() {
        assertTrue(Seasons.inWindow(MonthDay.of(12, 10), MonthDay.of(1, 5), LocalDate.of(2027, 1, 2)));
        assertFalse(Seasons.inWindow(MonthDay.of(12, 10), MonthDay.of(1, 5), LocalDate.of(2027, 2, 2)));
        assertTrue(Seasons.inWindow(MonthDay.of(7, 1), MonthDay.of(7, 31), LocalDate.of(2027, 7, 15)));
    }
}
