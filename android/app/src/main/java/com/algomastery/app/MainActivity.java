package com.algomastery.app;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.HorizontalScrollView;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Set;

/** Native, offline-friendly Android learning cockpit. */
public class MainActivity extends Activity {
    private static final int BG = Color.rgb(11, 13, 18);
    private static final int SURFACE = Color.rgb(21, 25, 35);
    private static final int RAISED = Color.rgb(27, 32, 48);
    private static final int BORDER = Color.rgb(39, 45, 59);
    private static final int TEXT = Color.rgb(245, 247, 255);
    private static final int MUTED = Color.rgb(155, 164, 181);
    private static final int VIOLET = Color.rgb(120, 107, 255);
    private static final int CYAN = Color.rgb(57, 213, 242);
    private static final int GREEN = Color.rgb(87, 208, 154);

    private final List<AlgorithmCatalog.Algorithm> allAlgorithms = AlgorithmCatalog.all();
    private SharedPreferences preferences;
    private String activeCategory = "All topics";
    private String searchTerm = "";
    private LinearLayout appRoot;
    private EditText searchInput;
    private Handler handler;
    private Runnable playRunnable;
    private BubbleState bubbleState;

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        getWindow().setStatusBarColor(BG);
        getWindow().setNavigationBarColor(BG);
        preferences = getSharedPreferences("algo-mastery", MODE_PRIVATE);
        handler = new Handler();
        showCatalog();
    }

    @Override public void onBackPressed() {
        if (bubbleState != null) stopBubblePlay();
        if (appRoot != null && appRoot.getTag() != null && "detail".equals(appRoot.getTag())) {
            bubbleState = null;
            showCatalog();
        } else {
            super.onBackPressed();
        }
    }

    private void showCatalog() {
        stopBubblePlay();
        bubbleState = null;
        appRoot = baseRoot();
        appRoot.setTag("catalog");
        appRoot.addView(header("ALGO-MASTERY", "Master the Logic. Own the Algorithm."));
        LinearLayout body = column(18, 16, 22, 24);
        TextView intro = text("Your algorithm cockpit", 26, TEXT, true);
        body.addView(intro, params(-1, -2, 0, 0, 0, 6));
        TextView sub = text("Explore the real 56-module repository, keep useful lessons bookmarked, and trace a selected algorithm without a network connection.", 14, MUTED, false);
        body.addView(sub, params(-1, -2, 0, 0, 0, 16));
        searchInput = edit("Search algorithms", searchTerm);
        body.addView(searchInput, params(-1, 48, 0, 0, 0, 14));
        HorizontalScrollView categoryScroll = new HorizontalScrollView(this);
        categoryScroll.setHorizontalScrollBarEnabled(false);
        LinearLayout categoryRow = row(0, 0, 0, 0);
        for (String category : AlgorithmCatalog.categories()) {
            Button categoryButton = pill(category, category.equals(activeCategory));
            categoryButton.setOnClickListener(v -> { activeCategory = category; showCatalog(); });
            categoryRow.addView(categoryButton, params(-2, 38, 0, 0, 0, 8));
        }
        categoryScroll.addView(categoryRow);
        body.addView(categoryScroll, params(-1, 44, 0, 0, 0, 15));
        TextView moduleCount = text("", 11, MUTED, false);
        body.addView(moduleCount, params(-1, -2, 0, 0, 0, 9));
        LinearLayout list = column(0, 0, 0, 0);
        body.addView(list, params(-1, -2, 0, 0, 0, 0));
        ScrollView scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        scroll.addView(body);
        appRoot.addView(scroll, params(-1, 0, 0, 0, 0, 0, 1));
        setContentView(appRoot);
        renderCatalogList(list, moduleCount);
        searchInput.addTextChangedListener(new TextWatcher() {
            public void beforeTextChanged(CharSequence s, int start, int count, int after) { }
            public void onTextChanged(CharSequence s, int start, int before, int count) { searchTerm = s.toString(); renderCatalogList(list, moduleCount); }
            public void afterTextChanged(Editable s) { }
        });
    }

    private void renderCatalogList(LinearLayout list, TextView countView) {
        List<AlgorithmCatalog.Algorithm> visible = new ArrayList<>();
        String query = searchTerm.trim().toLowerCase(Locale.US);
        for (AlgorithmCatalog.Algorithm algorithm : allAlgorithms) {
            boolean categoryMatch = activeCategory.equals("All topics") || algorithm.category.equals(activeCategory);
            boolean queryMatch = query.length() == 0 || (algorithm.name + " " + algorithm.description + " " + algorithm.category).toLowerCase(Locale.US).contains(query);
            if (categoryMatch && queryMatch) visible.add(algorithm);
        }
        if (countView != null) countView.setText(visible.size() + " modules shown  ·  " + savedCount() + " saved locally");
        list.removeAllViews();
        if (visible.isEmpty()) {
            TextView empty = text("No module matches this search. Try another phrase or reset the category.", 13, MUTED, false);
            list.addView(empty, params(-1, -2, 12, 20, 12, 20));
            return;
        }
        for (AlgorithmCatalog.Algorithm algorithm : visible) list.addView(algorithmCard(algorithm), params(-1, -2, 0, 0, 0, 10));
    }

    private View algorithmCard(AlgorithmCatalog.Algorithm algorithm) {
        LinearLayout card = cardColumn(14, 14, 14, 14);
        LinearLayout top = row(0, 0, 0, 0);
        TextView category = text(algorithm.category.toUpperCase(Locale.US), 10, CYAN, true);
        top.addView(category, params(0, -2, 0, 0, 10, 0, 1));
        TextView bookmark = text(isSaved(algorithm.slug) ? "♥" : "♡", 22, isSaved(algorithm.slug) ? VIOLET : MUTED, false);
        bookmark.setGravity(Gravity.CENTER);
        bookmark.setOnClickListener(v -> { toggleSaved(algorithm.slug); bookmark.setText(isSaved(algorithm.slug) ? "♥" : "♡"); bookmark.setTextColor(isSaved(algorithm.slug) ? VIOLET : MUTED); });
        top.addView(bookmark, params(34, 34, 0, 0, 0, 0));
        card.addView(top, params(-1, 34, 0, 0, 0, 7));
        TextView title = text(algorithm.name, 18, TEXT, true);
        card.addView(title, params(-1, -2, 0, 0, 0, 5));
        TextView description = text(algorithm.description, 12, MUTED, false);
        card.addView(description, params(-1, -2, 0, 0, 0, 11));
        TextView metrics = text(algorithm.time + "   ·   " + algorithm.space + (algorithm.interactive ? "   ·   interactive lab" : ""), 10, algorithm.interactive ? GREEN : MUTED, false);
        card.addView(metrics, params(-1, -2, 0, 0, 0, 0));
        card.setOnClickListener(v -> showDetail(algorithm));
        return card;
    }

    private void showDetail(AlgorithmCatalog.Algorithm algorithm) {
        stopBubblePlay();
        appRoot = baseRoot();
        appRoot.setTag("detail");
        LinearLayout toolbar = row(12, 13, 12, 12);
        Button back = actionButton("‹  Catalog", false);
        back.setOnClickListener(v -> showCatalog());
        toolbar.addView(back, params(0, 42, 0, 0, 12, 0, 1));
        Button saved = actionButton(isSaved(algorithm.slug) ? "♥ Saved" : "♡ Save", isSaved(algorithm.slug));
        saved.setOnClickListener(v -> { toggleSaved(algorithm.slug); saved.setText(isSaved(algorithm.slug) ? "♥ Saved" : "♡ Save"); });
        toolbar.addView(saved, params(-2, 42, 0, 0, 0, 0));
        appRoot.addView(toolbar);
        LinearLayout body = column(18, 16, 24, 24);
        TextView category = text(algorithm.category.toUpperCase(Locale.US) + "  /  VERIFIED LESSON", 10, CYAN, true);
        body.addView(category, params(-1, -2, 0, 0, 0, 8));
        body.addView(text(algorithm.name, 31, TEXT, true), params(-1, -2, 0, 0, 0, 10));
        body.addView(text(algorithm.description, 14, MUTED, false), params(-1, -2, 0, 0, 0, 17));
        LinearLayout metrics = row(0, 0, 0, 0);
        metrics.addView(metric("TIME", algorithm.time), params(0, -2, 0, 0, 8, 0, 1));
        metrics.addView(metric("SPACE", algorithm.space), params(0, -2, 0, 0, 0, 0, 1));
        body.addView(metrics, params(-1, -2, 0, 0, 0, 18));
        LinearLayout explanation = cardColumn(15, 15, 15, 15);
        explanation.addView(text("The learning lens", 15, TEXT, true), params(-1, -2, 0, 0, 0, 8));
        explanation.addView(text("Read the repository contract before scaling the example. The implementation is intentionally explicit about validation, limits, return values, and edge cases.", 12, MUTED, false), params(-1, -2, 0, 0, 0, 13));
        explanation.addView(text("Example shape: " + exampleFor(algorithm), 12, CYAN, false), params(-1, -2, 0, 0, 0, 0));
        body.addView(explanation, params(-1, -2, 0, 0, 0, 14));
        if (algorithm.interactive) addBubbleLab(body);
        LinearLayout source = cardColumn(15, 15, 15, 15);
        source.addView(text("Source map", 15, TEXT, true), params(-1, -2, 0, 0, 0, 8));
        source.addView(text("Python · Java · C\n" + algorithm.source.replace(".py", ".{py,java,c}"), 11, MUTED, false), params(-1, -2, 0, 0, 0, 10));
        Button repo = actionButton("Open repository source ↗", false);
        repo.setOnClickListener(v -> openSource(algorithm));
        source.addView(repo, params(-1, 42, 0, 0, 0, 0));
        body.addView(source, params(-1, -2, 0, 0, 0, 0));
        ScrollView scroll = new ScrollView(this);
        scroll.addView(body);
        appRoot.addView(scroll, params(-1, 0, 0, 0, 0, 0, 1));
        setContentView(appRoot);
    }

    private void addBubbleLab(LinearLayout body) {
        bubbleState = new BubbleState(new int[]{7, 3, 5, 1, 8, 2});
        LinearLayout lab = cardColumn(15, 15, 15, 15);
        lab.addView(text("Interactive bubble-sort trace", 15, TEXT, true), params(-1, -2, 0, 0, 0, 5));
        lab.addView(text("A small native lab: step through comparisons, reset, or let it play.", 11, MUTED, false), params(-1, -2, 0, 0, 0, 12));
        TextView trace = text(bubbleText(), 13, CYAN, true);
        trace.setTypeface(Typeface.MONOSPACE);
        lab.addView(trace, params(-1, -2, 0, 0, 0, 13));
        LinearLayout controls = row(0, 0, 0, 0);
        Button reset = actionButton("Reset", false); reset.setOnClickListener(v -> { stopBubblePlay(); bubbleState.reset(); trace.setText(bubbleText()); });
        Button step = actionButton("Step →", true); step.setOnClickListener(v -> { stopBubblePlay(); bubbleState.step(); trace.setText(bubbleText()); });
        Button play = actionButton("Play", false); play.setOnClickListener(v -> { if (playRunnable == null) startBubblePlay(trace); });
        controls.addView(reset, params(0, 42, 0, 0, 0, 0, 1)); controls.addView(step, params(0, 42, 8, 0, 8, 0, 1)); controls.addView(play, params(0, 42, 0, 0, 0, 0, 1));
        lab.addView(controls, params(-1, 42, 0, 0, 0, 0));
        body.addView(lab, params(-1, -2, 0, 0, 0, 14));
    }

    private void startBubblePlay(TextView trace) {
        playRunnable = new Runnable() { @Override public void run() { if (bubbleState.done()) { playRunnable = null; return; } bubbleState.step(); trace.setText(bubbleText()); handler.postDelayed(this, 750); } };
        handler.post(playRunnable);
    }

    private void stopBubblePlay() { if (playRunnable != null) { handler.removeCallbacks(playRunnable); playRunnable = null; } }

    private String bubbleText() { return bubbleState.valuesAsString() + "\n" + (bubbleState.done() ? "Complete — sorted tail is stable." : "Compare index " + bubbleState.index + " and " + (bubbleState.index + 1)); }

    private void openSource(AlgorithmCatalog.Algorithm algorithm) {
        String path = algorithm.source.replace(" ", "%20");
        startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse("https://github.com/Vasista-surya/Algo-Mastery/blob/main/" + path)));
    }

    private String exampleFor(AlgorithmCatalog.Algorithm algorithm) {
        if (algorithm.slug.equals("bubble-sort")) return "[7, 3, 5, 1] → [1, 3, 5, 7]";
        if (algorithm.slug.equals("binary-search")) return "[1, 3, 7, 9], key 7 → index 2";
        if (algorithm.slug.equals("kadane")) return "[-2, 1, -3, 4, -1, 2, 1] → 6";
        return algorithm.name + " follows the documented category contract.";
    }

    private int savedCount() { return savedSlugs().size(); }
    private boolean isSaved(String slug) { return savedSlugs().contains(slug); }
    private Set<String> savedSlugs() { return new HashSet<>(preferences.getStringSet("bookmarks", new HashSet<String>())); }
    private void toggleSaved(String slug) { Set<String> saved = savedSlugs(); if (!saved.add(slug)) saved.remove(slug); preferences.edit().putStringSet("bookmarks", saved).apply(); }

    private LinearLayout baseRoot() { LinearLayout root = column(0, 0, 0, 0); root.setBackgroundColor(BG); return root; }

    private LinearLayout header(String title, String subtitle) {
        LinearLayout wrapper = column(16, 19, 16, 14);
        LinearLayout row = row(0, 0, 0, 0);
        TextView mark = text("A", 21, TEXT, true); mark.setGravity(Gravity.CENTER); mark.setBackground(round(VIOLET, 10));
        row.addView(mark, params(39, 39, 0, 0, 12, 0));
        LinearLayout copy = column(0, 0, 0, 0); copy.addView(text(title, 14, TEXT, true)); copy.addView(text(subtitle, 10, MUTED, false));
        row.addView(copy, params(0, -2, 0, 2, 0, 0, 1));
        wrapper.addView(row);
        return wrapper;
    }

    private LinearLayout metric(String label, String value) { LinearLayout box = cardColumn(10, 9, 10, 9); box.addView(text(label, 9, MUTED, true)); box.addView(text(value, 16, TEXT, true)); return box; }

    private Button pill(String label, boolean active) { Button button = actionButton(label, active); button.setTextSize(10); return button; }
    private Button actionButton(String label, boolean primary) { Button button = new Button(this); button.setAllCaps(false); button.setText(label); button.setTextColor(primary ? TEXT : MUTED); button.setTextSize(11); button.setTypeface(Typeface.DEFAULT, Typeface.BOLD); button.setGravity(Gravity.CENTER); button.setPadding(10, 0, 10, 0); button.setBackground(round(primary ? VIOLET : SURFACE, 10)); return button; }
    private EditText edit(String hint, String value) { EditText input = new EditText(this); input.setHint(hint); input.setText(value); input.setSingleLine(true); input.setTextColor(TEXT); input.setHintTextColor(MUTED); input.setTextSize(13); input.setPadding(14, 0, 14, 0); input.setBackground(round(SURFACE, 12)); return input; }
    private TextView text(String value, int size, int color, boolean bold) { TextView view = new TextView(this); view.setText(value); view.setTextSize(size); view.setTextColor(color); view.setGravity(Gravity.CENTER_VERTICAL); if (bold) view.setTypeface(Typeface.DEFAULT, Typeface.BOLD); return view; }
    private LinearLayout column(int left, int top, int right, int bottom) { LinearLayout layout = new LinearLayout(this); layout.setOrientation(LinearLayout.VERTICAL); layout.setPadding(dp(left), dp(top), dp(right), dp(bottom)); return layout; }
    private LinearLayout row(int left, int top, int right, int bottom) { LinearLayout layout = column(left, top, right, bottom); layout.setOrientation(LinearLayout.HORIZONTAL); return layout; }
    private LinearLayout cardColumn(int left, int top, int right, int bottom) { LinearLayout layout = column(left, top, right, bottom); layout.setBackground(round(SURFACE, 16)); return layout; }
    private GradientDrawable round(int color, int radius) { GradientDrawable drawable = new GradientDrawable(); drawable.setColor(color); drawable.setCornerRadius(dp(radius)); drawable.setStroke(dp(1), BORDER); return drawable; }
    private LinearLayout.LayoutParams params(int width, int height, int left, int top, int right, int bottom) { return params(width, height, left, top, right, bottom, 0); }
    private LinearLayout.LayoutParams params(int width, int height, int left, int top, int right, int bottom, float weight) { LinearLayout.LayoutParams p = new LinearLayout.LayoutParams(width, height, weight); p.setMargins(dp(left), dp(top), dp(right), dp(bottom)); return p; }
    private int dp(int value) { return Math.round(value * getResources().getDisplayMetrics().density); }

    private static final class BubbleState {
        final int[] original; int[] values; int end; int index;
        BubbleState(int[] values) { this.original = values.clone(); reset(); }
        void reset() { values = original.clone(); end = values.length - 1; index = 0; }
        boolean done() { return end <= 0; }
        void step() { if (done()) return; if (index >= end) { end--; index = 0; return; } if (values[index] > values[index + 1]) { int temp = values[index]; values[index] = values[index + 1]; values[index + 1] = temp; } index++; }
        String valuesAsString() { return Arrays.toString(values); }
    }
}
