package com.cbosses.command;

import com.cbosses.T;

import com.cbosses.CBossesPlugin;
import com.cbosses.fight.BossDef;
import com.cbosses.fight.BossService;
import com.cbosses.util.Text;
import org.bukkit.Bukkit;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.command.TabCompleter;
import org.bukkit.entity.Player;
import org.jetbrains.annotations.NotNull;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** /cbosses (aliases /cb, /bosses). Players see /cbosses next; everything else needs cbosses.admin. */
public final class BossCommand implements CommandExecutor, TabCompleter {
    private static final List<String> ADMIN = List.of("menu", "list", "spawn", "test", "stop", "selftest", "arena", "schedule", "chapter", "season", "finale", "reload", "info", "next", "help");
    private final CBossesPlugin plugin;
    private final BossMenu menu;

    public BossCommand(CBossesPlugin plugin, BossMenu menu) { this.plugin = plugin; this.menu = menu; }

    private BossService s() { return plugin.service(); }

    @Override
    public boolean onCommand(@NotNull CommandSender sender, @NotNull Command command, @NotNull String label, String @NotNull [] args) {
        String sub = args.length == 0 ? (sender.hasPermission("cbosses.admin") && sender instanceof Player ? "menu" : "next") : args[0].toLowerCase(Locale.ROOT);
        if (sub.equals("next") || sub.equals("info")) { s().info(sender); return true; }
        if (sub.equals("chapter") && args.length >= 2 && args[1].equalsIgnoreCase("retry") && sender instanceof Player p) {
            if (!plugin.chapters().retry(p)) plugin.send(p, T.t("command.no-chapter-boss-is-waiting", "<gray>No chapter boss is waiting for you."));
            return true;
        }
        if (!sender.hasPermission("cbosses.admin")) { plugin.send(sender, T.t("command.you-can-t-use-that", "<red>You can't use that. <gray>Try /<label> next", "label", label)); return true; }
        Player player = sender instanceof Player p ? p : null;
        switch (sub) {
            case "menu", "gui" -> { if (player == null) plugin.send(sender, T.t("command.players-only", "<red>Players only.")); else menu.open(player, 0); }
            case "list" -> s().listBosses(sender);
            case "spawn" -> {
                if (args.length < 2) { plugin.send(sender, T.t("command.spawn-arena", "<yellow>/<label> spawn <boss> [arena]", "label", label)); return true; }
                String arena = args.length > 2 ? args[2] : plugin.getConfig().getString("schedule.arena", "main");
                BossDef def = s().def(args[1]);
                var a = s().arena(arena, false);
                if (def == null) plugin.send(sender, T.t("command.no-boss", "<red>No boss <input>", "input", Text.escape(args[1])));
                else if (a == null) plugin.send(sender, T.t("command.no-arena", "<red>No arena <arena>", "arena", Text.escape(arena)));
                else if (s().spawn(def, a, player, false, null)) plugin.send(sender, T.t("command.is-rising-at", "<green><boss> <green>is rising at <arena>.", "boss", def.name(), "arena", a.id));
            }
            case "test" -> {
                if (player == null) { plugin.send(sender, T.t("command.players-only-console-can-run", "<red>Players only. Console can run /<label> selftest.", "label", label)); return true; }
                if (args.length < 2) { plugin.send(player, T.t("command.test-phase-stop", "<yellow>/<label> test <boss>|phase|stop", "label", label)); return true; }
                switch (args[1].toLowerCase(Locale.ROOT)) {
                    case "stop" -> { if (!s().testStop(player)) plugin.send(player, T.t("command.you-have-no-test-boss", "<gray>You have no test boss.")); }
                    case "phase" -> { if (!s().testPhase(player)) plugin.send(player, T.t("command.you-have-no-test-boss", "<gray>You have no test boss.")); }
                    default -> s().test(player, args[1]);
                }
            }
            case "stop" -> {
                if (args.length < 2) { s().stopAll(); plugin.send(sender, T.t("command.every-boss-was-sent-away", "<gray>Every boss was sent away.")); return true; }
                if (!s().stop(args[1]) && !s().stopBoss(args[1].toLowerCase(Locale.ROOT))) plugin.send(sender, T.t("command.nothing-to-stop-called", "<gray>Nothing to stop called <input>.", "input", Text.escape(args[1])));
            }
            case "selftest" -> { plugin.send(sender, T.t("command.running-the-boss-self-test", "<gray>Running the boss self-test near the world spawn (takes about a minute)...")); s().selfTest(sender); }
            case "arena" -> arena(sender, player, label, args);
            case "schedule" -> {
                if (args.length >= 2 && (args[1].equalsIgnoreCase("on") || args[1].equalsIgnoreCase("off"))) s().scheduleToggle(sender, args[1].equalsIgnoreCase("on"));
                else s().info(sender);
            }
            case "chapter" -> {
                if (args.length >= 3 && args[1].equalsIgnoreCase("reset")) {
                    var target = Bukkit.getOfflinePlayer(args[2]);
                    plugin.chapters().reset(target.getUniqueId());
                    plugin.send(sender, T.t("command.chapter-bosses-reset-for", "<gray>Chapter bosses reset for <input2>.", "input2", Text.escape(args[2])));
                    return true;
                }
                if (args.length < 3) { plugin.send(sender, T.t("command.chapter-reset-retry", "<yellow>/<label> chapter <player> <chapter> <gray>| reset <player> | retry", "label", label)); return true; }
                Player target = Bukkit.getPlayerExact(args[1]);
                int n;
                try { n = Integer.parseInt(args[2]); } catch (NumberFormatException e) { plugin.send(sender, T.t("command.chapter-must-be-a-number", "<red>Chapter must be a number.")); return true; }
                if (target == null) { plugin.send(sender, T.t("command.is-not-online", "<red><input> is not online.", "input", Text.escape(args[1]))); return true; }
                if (plugin.chapters().bossFor(n) == null) { plugin.send(sender, T.t("command.no-boss-for-chapter", "<red>No boss for chapter <n>.", "n", n)); return true; }
                plugin.send(sender, plugin.chapters().trigger(target, n, true) ? T.t("command.chapter-boss-coming", "<green>Chapter <n> boss is coming for <player>.", "n", n, "player", target.getName()) : T.t("command.they-already-have-a-boss", "<yellow>They already have a boss coming."));
            }
            case "season", "seasons" -> plugin.seasons().command(sender, args);
            case "finale" -> {
                String what = args.length > 1 ? args[1].toLowerCase(Locale.ROOT) : "info";
                switch (what) {
                    case "wake" -> plugin.send(sender, plugin.finale().wake(true) ? T.t("command.finale-waking", "<light_purple>The finale is waking.") : T.t("command.finale-already", "<gray>The finale is already on its way, or its boss is missing."));
                    case "reset" -> { plugin.finale().reset(); plugin.send(sender, T.t("command.finale-reset", "<gray>Finale progress reset: every legend must be beaten again.")); }
                    default -> plugin.finale().info(sender);
                }
            }
            case "reload" -> { plugin.reloadAll(); plugin.send(sender, T.t("command.reloaded-bosses", "<green>Reloaded: <count> bosses.", "count", s().defs().size())); }
            default -> help(sender, label);
        }
        return true;
    }

    private void arena(CommandSender sender, Player player, String label, String[] args) {
        if (args.length < 2 || args[1].equalsIgnoreCase("list")) { s().listArenas(sender); return; }
        String action = args[1].toLowerCase(Locale.ROOT);
        String id = args.length > 2 ? args[2] : "main";
        switch (action) {
            case "setspawn" -> { if (player == null) plugin.send(sender, T.t("command.players-only", "<red>Players only.")); else s().setSpawn(player, id); }
            case "wand" -> { if (player == null) plugin.send(sender, T.t("command.players-only", "<red>Players only.")); else s().giveWand(player, id); }
            case "show" -> {
                var a = s().arena(id, false);
                if (player == null || a == null) plugin.send(sender, T.t("command.no-arena-2", "<red>No arena <id>", "id", Text.escape(id))); else s().show(player, a);
            }
            case "region" -> s().setRegion(sender, id, args.length > 3 ? args[3] : null);
            case "radius" -> {
                try { s().setRadius(sender, id, Integer.parseInt(args.length > 3 ? args[3] : "40")); }
                catch (NumberFormatException e) { plugin.send(sender, T.t("command.radius-must-be-a-number", "<red>Radius must be a number.")); }
            }
            case "clear" -> s().clearBorder(sender, id);
            case "delete" -> s().deleteArena(sender, id);
            default -> plugin.send(sender, T.t("command.arena-setspawn-wand-show-region", "<yellow>/<label> arena setspawn|wand|show|region|radius|clear|delete|list <arena>", "label", label));
        }
    }

    private void help(CommandSender to, String label) {
        String l = "/" + label;
        plugin.send(to, T.t("command.cbosses-commands", "<gold>CBosses commands"));
        String[][] lines = {
                {"menu", "<cmd> menu <gray>every boss in a menu"},
                {"list", "<cmd> list <gray>boss ids"},
                {"test", "<cmd> test <boss>|phase|stop <gray>try a boss in front of you, nothing is paid"},
                {"spawn", "<cmd> spawn <boss> [arena] <gray>start a real fight"},
                {"stop", "<cmd> stop [arena|boss] <gray>send bosses away"},
                {"arena", "<cmd> arena setspawn|wand|region|radius|show|clear|delete <arena>"},
                {"schedule", "<cmd> schedule on|off <gray>the weekly boss"},
                {"chapter", "<cmd> chapter <player> <n> | reset <player> | retry"},
                {"season", "<cmd> season <id> on|off|auto"},
                {"finale", "<cmd> finale [wake|reset] <gray>the boss after the three legends"},
                {"selftest", "<cmd> selftest <gray>spawn every boss, run every attack and death"},
                {"reload", "<cmd> reload"}};
        for (String[] line : lines)
            to.sendMessage(Text.mm(T.t("command.help." + line[0], " <yellow>" + line[1], "cmd", l)));
    }

    @Override
    public List<String> onTabComplete(@NotNull CommandSender sender, @NotNull Command command, @NotNull String alias, String @NotNull [] args) {
        if (!sender.hasPermission("cbosses.admin")) return args.length == 1 ? filter(List.of("next", "chapter"), args[0]) : List.of();
        if (args.length == 1) return filter(ADMIN, args[0]);
        String sub = args[0].toLowerCase(Locale.ROOT);
        if (args.length == 2) return switch (sub) {
            case "spawn" -> filter(s().ids(), args[1]);
            case "test" -> { List<String> out = new ArrayList<>(s().ids()); out.add("phase"); out.add("stop"); yield filter(out, args[1]); }
            case "stop" -> { List<String> out = new ArrayList<>(s().arenaIds()); out.addAll(s().ids()); yield filter(out, args[1]); }
            case "arena" -> filter(List.of("setspawn", "wand", "show", "region", "radius", "clear", "delete", "list"), args[1]);
            case "schedule" -> filter(List.of("on", "off"), args[1]);
            case "finale" -> filter(List.of("info", "wake", "reset"), args[1]);
            case "season", "seasons" -> filter(plugin.seasons().ids(), args[1]);
            case "chapter" -> { List<String> out = new ArrayList<>(List.of("reset", "retry")); for (Player p : Bukkit.getOnlinePlayers()) out.add(p.getName()); yield filter(out, args[1]); }
            default -> List.of();
        };
        if (args.length == 3) return switch (sub) {
            case "spawn", "arena" -> filter(s().arenaIds(), args[2]);
            case "season", "seasons" -> filter(List.of("on", "off", "auto"), args[2]);
            case "chapter" -> filter(List.of("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"), args[2]);
            default -> List.of();
        };
        return List.of();
    }

    static List<String> filter(List<String> options, String typed) {
        String t = typed.toLowerCase(Locale.ROOT);
        List<String> out = new ArrayList<>();
        for (String o : options) if (o.toLowerCase(Locale.ROOT).startsWith(t)) out.add(o);
        return out;
    }
}
