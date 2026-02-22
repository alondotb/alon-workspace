Context: VRT (Virtual Techies) — coding education platform for kids 10-14. Hebrew RTL, light theme, gamified, purple accent #6C3AED. Design these 4 core learning screens:

Screen 1 — Quest Map / Campaign Dashboard /quests (THE HERO SCREEN)
A visual 2D campaign map showing 28 quest nodes connected by winding paths — like a board game adventure map. Lush illustrated background (green hills, clouds, trees). Always-visible HUD bar at top: avatar portrait (small circle), level badge "Lv7" + title, animated XP progress bar (purple fill), coin balance "🪙 150", streak counter "🔥 5".

Quest node states on the map:
- Locked: grey circle, lock icon, dim
- Available: glowing pulsing bright circle with star
- In Progress: arrow icon, circular progress ring around it
- Completed: checkmark, gold star, full color
- Current active: largest node, animated purple glow

Progress indicator "12/28 Quests" with bar. The map scrolls/pans. Show approximately 8-10 visible nodes with paths connecting them.

Screen 2 — Quest Briefing /quests/:id/briefing
Clean card layout. Back arrow top-left. Quest title large. Description paragraph in Hebrew. "What you'll learn:" bullet list (3-4 items). Estimated time "⏱️ 15 min". Question requirement "Pass 5 of 6 to unlock next quest". Big purple "Start Quest" button at bottom.

Screen 3 — Coding Workspace /quests/:id/learn (CORE EXPERIENCE)
Split layout. Left panel: scrollable lesson content — Hebrew RTL text with headings, paragraphs, code examples. Right panel: interactive code editor (Monaco-style, light theme, Python code visible, line numbers, syntax highlighting). Below editor: green "▶ Run" button and grey "↺ Reset" button side by side. Below buttons: output panel (dark background, monospace text showing "Hello World!" output with green left border for success). Navigation at bottom: "← Previous" and "Next →" buttons. Top bar: "📝 5/6 questions completed" with small progress bar.

Screen 4 — Question: Code Write
Full-width layout. Top: "Question 3/6" + difficulty badge (green pill "Easy" or yellow "Medium"). Prompt text in Hebrew: instructions for what to code. Code editor below (empty or with starter code). Three buttons: purple "Submit", yellow "💡 Hint", grey "Skip →".

Show all 4 screens in a 2x2 grid.
