package com.cbosses;

import com.cbosses.api.CBossesAPI;
import com.cbosses.chapter.ChapterBosses;
import com.cbosses.command.BossCommand;
import com.cbosses.command.BossMenu;
import com.cbosses.fight.BossService;
import com.cbosses.fight.Fx;
import com.cbosses.hook.WorldGuardHook;
import com.cbosses.season.Seasons;
import com.cbosses.util.Sched;
import com.cbosses.util.Text;
import org.bukkit.command.CommandSender;
import org.bukkit.configuration.file.YamlConfiguration;
import org.bukkit.plugin.java.JavaPlugin;

import java.io.File;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

/** CBosses: animated block-model bosses with weekly, seasonal and chapter fights. Paper and Folia. */
public final class CBossesPlugin extends JavaPlugin {
    private static CBossesPlugin instance;
    private BossService service;
    private ChapterBosses chapters;
    private Seasons seasons;
    private CBossesAPI api;
    private YamlConfiguration messages = new YamlConfiguration();

    public static CBossesPlugin instance() { return instance; }

    @Override
    public void onLoad() {
        // WorldGuard flags can only be registered before WorldGuard enables.
        if (getServer().getPluginManager().getPlugin("WorldGuard") != null) WorldGuardHook.registerFlags(getLogger());
    }

    @Override
    public void onEnable() {
        instance = this;
        saveDefaultConfig();
        getConfig().options().copyDefaults(true);
        saveConfig();
        if (!new File(getDataFolder(), "bosses.yml").exists()) saveResource("bosses.yml", false);
        if (!new File(getDataFolder(), "messages.yml").exists()) saveResource("messages.yml", false);
        loadMessages();
        Sched.init(this);
        Fx.init(this);
        WorldGuardHook.init(getServer().getPluginManager().getPlugin("WorldGuard") != null && getConfig().getBoolean("worldguard.enabled", true), getLogger());
        seasons = new Seasons(this);
        service = new BossService(this);
        chapters = new ChapterBosses(this);
        api = new CBossesAPI(this);
        getServer().getPluginManager().registerEvents(service, this);
        getServer().getPluginManager().registerEvents(chapters, this);
        BossMenu menu = new BossMenu(this);
        getServer().getPluginManager().registerEvents(menu, this);
        BossCommand command = new BossCommand(this, menu);
        var cmd = getCommand("cbosses");
        if (cmd != null) { cmd.setExecutor(command); cmd.setTabCompleter(command); }
        service.start();
        if (getServer().getPluginManager().getPlugin("PlaceholderAPI") != null) {
            try { new com.cbosses.hook.Placeholders(this).register(); getLogger().info("PlaceholderAPI placeholders registered (%cbosses_...%)."); }
            catch (Throwable e) { getLogger().warning("Could not register placeholders: " + e); }
        }
        getLogger().info("CBosses " + getPluginMeta().getVersion() + " enabled with " + service.defs().size() + " bosses"
                + (WorldGuardHook.available() ? ", WorldGuard support on" : "")
                + (getServer().getPluginManager().getPlugin("CQuests") != null ? ", CQuests chapter bosses on" : "") + ".");
    }

    @Override
    public void onDisable() {
        if (service != null) service.shutdown();
    }

    public void reloadAll() {
        reloadConfig();
        loadMessages();
        service.reload();
        service.start();
    }

    private void loadMessages() {
        File file = new File(getDataFolder(), "messages.yml");
        messages = YamlConfiguration.loadConfiguration(file);
        try (var in = getResource("messages.yml")) {
            if (in != null) messages.setDefaults(YamlConfiguration.loadConfiguration(new InputStreamReader(in, StandardCharsets.UTF_8)));
        } catch (Exception ignored) { }
    }

    public String msg(String key, String fallback) {
        String s = messages.getString(key);
        return s == null ? fallback : s;
    }

    public void send(CommandSender to, String miniMessage) {
        if (to == null) return;
        to.sendMessage(Text.mm(msg("prefix", "<dark_gray>[<gold>CBosses</gold>]</dark_gray> ") + miniMessage));
    }

    public BossService service() { return service; }
    public ChapterBosses chapters() { return chapters; }
    public Seasons seasons() { return seasons; }
    public CBossesAPI api() { return api; }
}
