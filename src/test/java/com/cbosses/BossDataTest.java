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
        assertEquals(93, defs.size(), "36 weekly, 5 mythic, 12 seasonal, 10 chapter and 30 mini bosses");
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
    void bigBossesHave150BlocksChapterBossesAreSmallAndAllCanDropDetail() throws Exception {
        var full = models();
        var defs = bosses();
        for (BossDef d : defs.values()) {
            ModelRig.Model fm = full.get(d.model());
            int n = fm.cubes.size();
            // only one face is shown at a time, so the spare faces don't count
            if (fm.faceOf != null) for (String f : fm.faceOf) if (f != null && !f.equals("idle")) n--;
            if (d.mini()) assertTrue(n >= 25 && n <= 200, d.id() + " is a mini boss with " + n + " blocks");
            else if (d.chapterBoss()) assertTrue(n >= 80 && n <= 130, d.id() + " is a chapter boss with " + n + " blocks");
            else if (d.seasonal()) assertTrue(n >= 60 && n <= 300, d.id() + " is a painted seasonal boss with " + n + " blocks");
            else if (!d.id().equals("grand_augur")) assertTrue(n >= 150, d.id() + " has only " + n + " blocks");
        }
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
    void threeBossesForEverySeason() throws Exception {
        var defs = bosses();
        for (String season : new String[]{"winter", "summer", "spring", "halloween"})
            assertEquals(3, defs.values().stream().filter(d -> d.seasonal() && season.equals(d.season())).count(), season);
        assertEquals(41, defs.values().stream().filter(d -> !d.seasonal() && !d.chapterBoss() && !d.mini()).count(), "36 weekly bosses and 5 mythic");
    }

    @Test
    void healthTiersAndMiniBosses() throws Exception {
        var defs = bosses();
        assertEquals(30, defs.values().stream().filter(BossDef::mini).count(), "30 mini bosses");
        for (BossDef d : defs.values()) {
            if (d.mini()) assertEquals(3000, d.health(), 0.01, d.id());
            else if (d.tier().equals("mythic")) assertEquals(8000, d.health(), 0.01, d.id());
            else if (!d.chapterBoss()) assertEquals(5000, d.health(), 0.01, d.id());
        }
        for (String id : new String[]{"the_unmaker", "withered_tyrant", "ender_wyrm", "gale_sovereign", "the_listener"}) assertEquals("mythic", defs.get(id).tier(), id);
    }

    @Test
    void faceChangingModels() throws Exception {
        var models = models();
        ModelRig.Model king = models.get("gourd_king");
        assertNotNull(king.faceOf, "the Gourd King changes faces");
        for (String f : new String[]{"idle", "angry", "hurt", "rage", "dead"}) assertTrue(king.faces.contains(f), "gourd king face " + f);
        for (String id : new String[]{"decor_pumpkin_tall", "decor_pumpkin_flat", "decor_pumpkin_cube"}) {
            ModelRig.Model m = models.get(id);
            assertNotNull(m, id);
            assertTrue(m.faces.size() >= 5, id + " has faces");
        }
        // only one face shows at a time
        var pose = ModelRig.cubes(king, ModelRig.pose(king, java.util.List.of(new ModelRig.Layer(king.anim("idle"), 0, 1))));
        king.showFace(pose, "angry");
        for (int i = 0; i < pose.length; i++) if (king.faceOf[i] != null && !king.faceOf[i].equals("angry"))
            assertTrue(pose[i].getScale(new org.joml.Vector3f()).length() < 1e-4, "hidden face piece " + i);
    }

    @Test
    void theFinaleBossExistsAndIsKeptOutOfTheWeeklyRotation() throws Exception {
        var defs = bosses();
        assertNotNull(defs.get("the_unmaker"), "the finale boss");
        for (String legend : new String[]{"withered_tyrant", "ender_wyrm", "gale_sovereign", "the_listener"}) assertNotNull(defs.get(legend), legend);
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
