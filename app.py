import streamlit as st
import random
import pandas as pd
from enum import Enum
from dataclasses import dataclass, field
from typing import List


class PowerType(Enum):
    SOFT = "Soft Power"
    HARD = "Hard Power"
    SMART = "Smart Power"


class Tool(Enum):
    ETHOS = "Ethos"
    LOGOS = "Logos"
    PATHOS = "Pathos"
    ALLOCENTRISM = "Allocentrism"
    EXCHANGE = "Exchange"
    NETWORKS = "Networks"
    COALITIONS = "Coalitions"
    TEAM_BUILDING = "Team Building"
    MIGHT = "Might"
    INTENTIONALITY = "Intentionality"
    SITUATIONAL_AWARENESS = "Situational Awareness"
    AGENCY = "Agency"


@dataclass
class ToolCard:
    tool: Tool
    power_type: PowerType
    points_value: int
    effect: str
    description: str


@dataclass
class ScenarioCard:
    name: str
    situation: str
    suggested_tools: List[Tool]
    reward_token: str
    lesson: str
    play_example: str


@dataclass
class Player:
    name: str
    influence_points: int = 0
    tokens: List[str] = field(default_factory=list)
    round_scores: List[int] = field(default_factory=list)
    reflections: List[str] = field(default_factory=list)

    def get_total_points(self):
        return self.influence_points

    def get_final_score(self):
        token_bonus = len(self.tokens) * 5
        return self.get_total_points() + token_bonus

    def add_round_score(self, score: int):
        self.round_scores.append(score)
        self.influence_points += score

    def add_token(self, token: str):
        self.tokens.append(token)

    def add_reflection(self, reflection: str):
        self.reflections.append(reflection)

    def get_token_count(self):
        return len(self.tokens)


class GameState:
    TOOLS = [
        ToolCard(
            Tool.ETHOS,
            PowerType.SOFT,
            2,
            "+2 Credibility Points when words and actions align",
            "Build integrity and trust through consistency.",
        ),
        ToolCard(
            Tool.LOGOS,
            PowerType.SMART,
            2,
            "+2 Clarity Points when you use logic and evidence",
            "Use reasoning and data to reduce ambiguity.",
        ),
        ToolCard(
            Tool.PATHOS,
            PowerType.SOFT,
            2,
            "+2 Influence Points when others remember your story",
            "Lead with emotion and storytelling to inspire others.",
        ),
        ToolCard(
            Tool.ALLOCENTRISM,
            PowerType.SOFT,
            2,
            "+2 Trust Points in collaborative challenges",
            "Listen before you lead — empathy builds influence.",
        ),
        ToolCard(
            Tool.EXCHANGE,
            PowerType.HARD,
            2,
            "+2 Reciprocity Points when you trade value fairly",
            "Negotiate by creating mutual benefit.",
        ),
        ToolCard(
            Tool.NETWORKS,
            PowerType.SOFT,
            3,
            "+3 Connection Points through alliances",
            "Build bridges early; relationships drive influence.",
        ),
        ToolCard(
            Tool.COALITIONS,
            PowerType.SMART,
            3,
            "+3 Alliance Points when you prepare together",
            "Have the meeting before the meeting. Collaboration wins.",
        ),
        ToolCard(
            Tool.TEAM_BUILDING,
            PowerType.SOFT,
            3,
            "+3 Cohesion Points when fostering inclusion",
            "Unite diverse strengths under a shared goal.",
        ),
        ToolCard(
            Tool.MIGHT,
            PowerType.HARD,
            3,
            "+3 Authority Points when decisive action is needed",
            "Use authority responsibly; direct when urgency demands it.",
        ),
        ToolCard(
            Tool.INTENTIONALITY,
            PowerType.SMART,
            2,
            "Skip one draw to double next play's points (+2 bonus)",
            "Focus on priorities — trade lesser goals for greater ones.",
        ),
        ToolCard(
            Tool.SITUATIONAL_AWARENESS,
            PowerType.SMART,
            3,
            "+3 Insight Points when adapting to context",
            "Read the room: assess timing, dynamics, and readiness before acting.",
        ),
        ToolCard(
            Tool.AGENCY,
            PowerType.SMART,
            3,
            "+3 Adaptability Points for proactive leadership",
            "Shape the situation rather than reacting to it.",
        ),
    ]

    SCENARIOS = [
        ScenarioCard(
            "Sergio de Mello — Empowering Others",
            "You're leading a humanitarian project in a region where local staff distrust external leaders. You have authority from headquarters, but the community sees you as an outsider. Trust is low, buy-in is absent, and without local partnership, your project will fail. The challenge is to earn legitimacy by genuinely empowering locals rather than imposing solutions.",
            [Tool.AGENCY, Tool.ALLOCENTRISM, Tool.INTENTIONALITY],
            "Legitimacy Token",
            "Real influence means building legitimacy, not authority. When leaders listen, adapt, and give others genuine ownership, trust becomes their strongest source of power.",
            "You begin by asking local staff what success means to them (Allocentrism). Instead of dictating, you adapt project rules to fit cultural practices (Agency). You clarify the long-term mission — rebuilding communities with fairness — so everyone feels ownership (Intentionality).",
        ),
        ScenarioCard(
            "Erik Peterson — Conflict & Collaboration",
            "Two of your senior managers are fighting bitterly over marketing budgets. One leads product, the other leads sales. Both feel threatened; both want resources for their vision. The conflict is now spilling into meetings, frustrating teams, and threatening a critical product launch.",
            [Tool.PATHOS, Tool.NETWORKS, Tool.ALLOCENTRISM],
            "Cohesion Token",
            "Great leaders don't just solve conflicts — they heal them. Influence comes from aligning emotions, relationships, and purpose so that disagreement turns into shared drive.",
            "You meet each manager privately to understand their concerns (Allocentrism). You reframe the dispute using a story about shared goals (Pathos). Then, you engage informal allies to support collaboration (Networks).",
        ),
        ScenarioCard(
            "Leading Change — Overcoming Resistance",
            "You've introduced a new system designed to improve efficiency and collaboration. But adoption has stalled. Employees are skeptical, some are actively resistant, and rumors spread that the change is being forced from above.",
            [Tool.COALITIONS, Tool.AGENCY, Tool.INTENTIONALITY],
            "Buy-In Token",
            "Change is less about plans and more about participation. When people are included, understand the 'why,' and see early success, resistance transforms into commitment.",
            "You start by engaging early supporters to model new behavior (Coalitions). You launch a small pilot to show results (Agency). You clearly explain how the change connects to long-term vision (Intentionality).",
        ),
        ScenarioCard(
            "Cross-Functional Merger — Onboarding",
            "Two companies have just merged. The teams are now sharing offices, processes, and leadership. But they come from different cultures: one was fast-moving and entrepreneurial, the other was structured and risk-averse. People feel their identity is threatened.",
            [Tool.ALLOCENTRISM, Tool.COALITIONS, Tool.TEAM_BUILDING],
            "Integration Token",
            "Integration isn't about blending identities; it's about respecting differences while forging unity. Influence here means empathy first, collaboration second, and shared celebration third.",
            "You hold listening sessions to surface frustrations and hopes (Allocentrism). You form a cross-team task force to align processes (Coalitions). You close the week with a team-building session celebrating shared wins (Team Building).",
        ),
        ScenarioCard(
            "Remote Team — Burnout Warning",
            "Your distributed team has been remote for two years. Productivity is strong, but you're noticing warning signs: people are taking longer to respond, meetings feel perfunctory, and some top performers are quietly job-hunting.",
            [Tool.PATHOS, Tool.INTENTIONALITY, Tool.ALLOCENTRISM],
            "Resilience Token",
            "Remote leadership thrives on human connection. Empathy, focus, and honesty rebuild motivation more effectively than deadlines or incentives.",
            "You start the meeting with appreciation and openness about fatigue (Pathos). You cut nonessential projects to refocus on priorities (Intentionality). You hold listening sessions to understand personal challenges (Allocentrism).",
        ),
        ScenarioCard(
            "Regulatory Approval — Evidence & Allies",
            "You've developed an innovative pilot program that could transform your industry, but it requires regulatory approval. The regulator is cautious, skeptical, and has been burned by false promises before.",
            [Tool.LOGOS, Tool.ETHOS, Tool.NETWORKS],
            "Credibility Token",
            "Influence is strongest when credibility, relationships, and reasoning work together. Facts alone persuade no one — but trusted messengers armed with logic can move institutions.",
            "You prepare a compelling evidence report highlighting safety and value (Logos). You partner with a respected industry figure to co-present (Ethos). You leverage existing professional connections to build informal trust (Networks).",
        ),
        ScenarioCard(
            "Product Recall — Public Trust",
            "A defect in your product has been discovered. Customers are affected, media is questioning your integrity, and regulators are involved. This is a crisis that tests your values under extreme pressure.",
            [Tool.ALLOCENTRISM, Tool.PATHOS, Tool.COALITIONS],
            "Trust Restoration Token",
            "Trust is rebuilt through transparency, care, and cooperation. In crisis, vulnerability is not weakness — it's the foundation of credibility.",
            "You listen to affected customers to understand their needs (Allocentrism). You express genuine empathy in public statements (Pathos). You coordinate teams and partners to manage repairs and communication (Coalitions).",
        ),
        ScenarioCard(
            "Budget Cuts — Stakeholder Alignment",
            "Your organization faces a 20% budget reduction due to market conditions. Every team lead wants to protect their projects. Resources are scarce; tradeoffs are inevitable.",
            [Tool.LOGOS, Tool.INTENTIONALITY, Tool.COALITIONS],
            "Alignment Token",
            "Scarcity can become strategic strength when framed as focus. Leadership influence means transforming fear into collective purpose.",
            "You reframe the situation as a chance to sharpen focus (Logos). You prioritize core projects that protect your mission (Intentionality). You bring all stakeholders together to co-decide adjustments (Coalitions).",
        ),
        ScenarioCard(
            "Inclusion Journey — Building Belonging",
            "Your organization launches a Diversity, Equity, and Inclusion (DEI) initiative. The intention is good, but resistance appears immediately. Some people see it as reverse discrimination, others dismiss it as performative.",
            [Tool.ALLOCENTRISM, Tool.TEAM_BUILDING, Tool.PATHOS],
            "Inclusion Token",
            "Inclusion is built through stories, standards, and listening. Influence here is moral as much as strategic — it's about shaping culture through consistent fairness and shared humanity.",
            "You invite open dialogue with skeptics (Allocentrism). You establish clear behavioral norms — respect, curiosity, and empathy (Team Building). You share stories from team members who've benefited from inclusion (Pathos).",
        ),
    ]


def init_session_state():
    if "game_started" not in st.session_state:
        st.session_state.game_started = False
    if "players" not in st.session_state:
        st.session_state.players = []
    if "current_round" not in st.session_state:
        st.session_state.current_round = 0
    if "max_rounds" not in st.session_state:
        st.session_state.max_rounds = 5
    if "current_scenario" not in st.session_state:
        st.session_state.current_scenario = None
    if "current_player_index" not in st.session_state:
        st.session_state.current_player_index = 0
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "reflection_prompts" not in st.session_state:
        st.session_state.reflection_prompts = [
            "Where did listening or empathy change your approach?",
            "How did storytelling or logic influence your choice?",
            "What alliances or norms did you strengthen?",
            "What situational cues guided your timing?",
            "How did your decisions align with fairness, awareness, or ownership?",
        ]
    if "scenario_pool" not in st.session_state:
        st.session_state.scenario_pool = list(GameState.SCENARIOS)
        random.shuffle(st.session_state.scenario_pool)


def calculate_points(chosen_tools, scenario):
    base_points = sum(tool.points_value for tool in chosen_tools)
    synergy_bonus = (
        2
        if sum(1 for tool in chosen_tools if tool.tool in scenario.suggested_tools) >= 2
        else 0
    )
    variety_bonus = 1 if len(set(tool.power_type for tool in chosen_tools)) == 3 else 0
    total = base_points + synergy_bonus + variety_bonus
    return base_points, synergy_bonus, variety_bonus, total


def main():
    st.set_page_config(
        page_title="The Strategy Shuffle",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    init_session_state()

    st.markdown(
        """
    <style>
    .stApp {background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);}
    [data-testid="stSidebar"] {background: linear-gradient(180deg, #e0d4f7 0%, #d8c5f0 100%); color: #2d1b69;}
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4, [data-testid="stSidebar"] label {color: #2d1b69 !important;}
    .stButton>button {background: linear-gradient(135deg, #a7c4f7 0%, #b8a5e8 100%); color: #2d1b69; font-weight: 600;}
    .stButton>button:hover {transform: translateY(-2px); box-shadow: 0 8px 16px rgba(167, 196, 247, 0.3);}
    .stTextArea textarea, .stTextInput input {background-color: #ffffff !important; border: 2px solid #d0c5f7 !important; border-radius: 8px !important; color: #2d1b69 !important;}
    </style>
    """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown("### 📋 My Influence Profile")
        st.markdown("---")
        st.markdown("#### 🔝 Top Strengths")
        my_strengths = st.multiselect(
            "My Strengths",
            options=[t.value for t in Tool],
            max_selections=5,
            key="my_strength_tools",
            default=[
                "Allocentrism",
                "Agency",
                "Intentionality",
                "Situational Awareness",
                "Ethos",
            ],
        )
        st.markdown("#### 🌱 Growth Opportunities")
        my_growth = st.multiselect(
            "Areas to Grow",
            options=[t.value for t in Tool],
            max_selections=3,
            key="my_growth_tools",
            default=["Networks", "Might", "Exchange"],
        )
        st.markdown("#### 🎯 Personal Focus")
        my_goal = st.text_area(
            "My Focus for This Game",
            "Practice early influence, not reactive influence. Use my growth tools — especially Networks and Might — in at least two scenarios to strengthen balance between empathy and assertiveness.",
            height=150,
            key="my_personal_goal",
        )
        st.markdown("#### 💪 Power Style")
        my_style = st.text_area(
            "My Influence Style",
            "Smart Power Integrator — I combine structure, empathy, and foresight. I tend to lead through understanding, preparation, and fairness.",
            height=150,
            key="my_power_style",
        )

    st.title("🃏 The Strategy Shuffle")
    st.subheader("A Leadership & Influence Card Game")
    st.markdown("**Master influence through strategic, empathetic decision-making**")
    st.markdown("---")
    st.markdown("""
    ### 🎯 What This Game Is
    This game is my personal distillation of the Managerial Decision-Making and Influence course. It turns lessons on **Soft, Hard, and Smart Power** into an interactive reflection tool.
    My Leverage Inventory shows strong **Smart Power** — empathy, awareness, and focus — and areas to grow in **Networks** and **Might**. Each round helps me practice new influence tools while reinforcing fairness, awareness, and ownership.
    I built this to guide my future self — **to listen deeply, act intentionally, and lead with balance.**
    """)

    tab1, tab2 = st.tabs(["🎮 Play Game", "🧰 Tool Guide"])

    with tab2:
        st.markdown("## 🧰 The 12 Influence Tools")
        tools_data = [
            {
                "Tool": "Ethos",
                "Power Type": "Soft Power",
                "Description": "Lead with credibility and integrity.",
                "Key Idea": "Influence through trust and consistency.",
            },
            {
                "Tool": "Logos",
                "Power Type": "Smart Power",
                "Description": "Use logic, evidence, and reasoning.",
                "Key Idea": "Persuade through clarity and proof.",
            },
            {
                "Tool": "Pathos",
                "Power Type": "Soft Power",
                "Description": "Communicate with emotion and story.",
                "Key Idea": "Inspire through connection, not data.",
            },
            {
                "Tool": "Allocentrism",
                "Power Type": "Soft / Smart Power",
                "Description": "Listen before leading; understand others' perspectives.",
                "Key Idea": "Empathy creates influence.",
            },
            {
                "Tool": "Exchange",
                "Power Type": "Hard / Smart Power",
                "Description": "Create mutual value through fair tradeoffs.",
                "Key Idea": "Reciprocity strengthens relationships.",
            },
            {
                "Tool": "Networks",
                "Power Type": "Soft / Smart Power",
                "Description": "Build diverse, genuine connections.",
                "Key Idea": "Relationships are long-term power.",
            },
            {
                "Tool": "Coalitions",
                "Power Type": "Smart Power",
                "Description": "Align allies before the meeting.",
                "Key Idea": "Collaboration shapes decisions.",
            },
            {
                "Tool": "Team Building",
                "Power Type": "Soft Power",
                "Description": "Foster unity and shared purpose.",
                "Key Idea": "Cohesion sustains influence.",
            },
            {
                "Tool": "Might",
                "Power Type": "Hard Power",
                "Description": "Use authority decisively when needed.",
                "Key Idea": "Assertiveness can be ethical.",
            },
            {
                "Tool": "Intentionality",
                "Power Type": "Smart Power",
                "Description": "Focus energy on key goals.",
                "Key Idea": "Clarity beats busyness.",
            },
            {
                "Tool": "Situational Awareness",
                "Power Type": "Smart Power",
                "Description": "Read the room and adapt to context.",
                "Key Idea": "Awareness enables timing.",
            },
            {
                "Tool": "Agency",
                "Power Type": "Smart Power",
                "Description": "Take initiative; shape situations.",
                "Key Idea": "Don't wait — act with purpose.",
            },
        ]

        for tool in tools_data:
            with st.expander(f"**{tool['Tool']}** — {tool['Power Type']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Description:** {tool['Description']}")
                with col2:
                    st.write(f"**Key Idea:** {tool['Key Idea']}")

    with tab1:
        if not st.session_state.game_started:
            st.markdown("---")
            st.markdown("## 📖 Game Setup")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 👥 Number of Players")
                num_players = st.slider(
                    "How many players?", 1, 6, 2, label_visibility="collapsed"
                )
            with col2:
                st.markdown("### 🔄 Number of Rounds")
                num_rounds = st.slider(
                    "How many rounds?", 1, 9, 5, label_visibility="collapsed"
                )

            st.markdown("### 🎭 Player Names")
            player_names = []
            cols = st.columns(2)
            for i in range(num_players):
                with cols[i % 2]:
                    name = st.text_input(
                        f"Player {i + 1}",
                        value=f"Player {i + 1}",
                        key=f"player_name_{i}",
                        label_visibility="collapsed",
                    )
                    player_names.append(name)

            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button(
                    "🎮 Start Game", key="start_button", use_container_width=True
                ):
                    st.session_state.players = [Player(name) for name in player_names]
                    st.session_state.max_rounds = num_rounds
                    st.session_state.scenario_pool = list(GameState.SCENARIOS)
                    random.shuffle(st.session_state.scenario_pool)
                    st.session_state.game_started = True
                    st.session_state.current_round = 1
                    st.session_state.current_scenario = (
                        st.session_state.scenario_pool.pop(0)
                    )
                    st.rerun()

        elif st.session_state.game_over:
            st.markdown("---")
            st.markdown("# 🏆 Game Over!")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("## 🥇 Final Scores")
                players_data = [
                    {
                        "Player": p.name,
                        "Base Points": p.get_total_points(),
                        "Tokens": p.get_token_count(),
                        "Token Bonus": p.get_token_count() * 5,
                        "Final Score": p.get_final_score(),
                    }
                    for p in st.session_state.players
                ]
                df = pd.DataFrame(players_data).sort_values(
                    "Final Score", ascending=False
                )
                st.dataframe(df, use_container_width=True)

            with col2:
                winner = max(
                    st.session_state.players, key=lambda p: p.get_final_score()
                )
                st.markdown(f"### 👑 **{winner.name}**")
                col_w1, col_w2 = st.columns(2)
                with col_w1:
                    st.metric("Final Score", winner.get_final_score())
                with col_w2:
                    st.metric("Tokens Earned", winner.get_token_count())

                st.markdown("**Score Breakdown:**")
                st.write(f"  • Base Points: **{winner.get_total_points()}**")
                st.write(
                    f"  • Tokens: {winner.get_token_count()} × 5 = **+{winner.get_token_count() * 5}**"
                )
                st.write(f"  • **Total: {winner.get_final_score()}**")

            st.markdown("---")
            st.markdown("## 📊 Player Details")
            for player in st.session_state.players:
                with st.expander(f"👤 {player.name}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Final Score", player.get_final_score())
                    with col2:
                        st.metric("Base Points", player.get_total_points())
                    with col3:
                        st.metric("Tokens", player.get_token_count())

                    if player.tokens:
                        st.markdown("**🏆 Tokens Earned:**")
                        for token in player.tokens:
                            st.markdown(f"  ✨ {token}")

                    st.markdown(f"**Round Scores:** {player.round_scores}")

                    if player.reflections:
                        st.markdown(f"**💭 Reflections ({len(player.reflections)}):**")
                        for i, reflection in enumerate(player.reflections, 1):
                            st.write(f"**Round {i}:** _{reflection}_")
                    else:
                        st.write("*No reflections recorded*")

            st.markdown("---")
            st.markdown("## 🎓 Key Lessons")
            lessons = [
                "🎧 Empathy & Listening (Allocentrism) are powerful levers.",
                "🤝 Networking is about genuine connection, not charisma.",
                "🧠 Smart Power means knowing WHEN to use Soft & Hard power.",
                "🔄 Real change comes from fairness, inclusion, and ownership.",
                "🎯 Read the room (Situational Awareness) before acting.",
                "⚡ Shape situations (Agency) rather than just reacting.",
                "📖 Stories stick; data clarifies. Use both.",
                "💼 Build alliances BEFORE you need them (Coalitions).",
                "🤲 Give first; reciprocity builds loyalty.",
                "🌟 True influence is ethical, intentional, and generous.",
            ]
            for lesson in lessons:
                st.write(lesson)

            st.markdown("---")
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🔄 Play Again", use_container_width=True):
                    st.session_state.game_started = False
                    st.session_state.players = []
                    st.session_state.current_round = 0
                    st.session_state.game_over = False
                    st.session_state.current_player_index = 0
                    st.rerun()

        else:
            progress = (
                st.session_state.current_round - 1
            ) / st.session_state.max_rounds
            st.progress(progress)
            st.markdown(
                f"### 📍 Round {st.session_state.current_round} of {st.session_state.max_rounds}"
            )
            st.markdown("---")

            scenario = st.session_state.current_scenario
            current_player = st.session_state.players[
                st.session_state.current_player_index
            ]

            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"## 📋 {scenario.name}")
                st.markdown(scenario.situation)
                with st.expander("💡 **Suggested Tools & Lesson**"):
                    st.write(
                        f"**Suggested Tools:** {', '.join([t.value for t in scenario.suggested_tools])}"
                    )
                    st.write(f"**Reward Token:** ✨ {scenario.reward_token}")
                    st.write(f"**Play Example:** {scenario.play_example}")
                    st.write(f"**Lesson:** {scenario.lesson}")

            with col2:
                st.markdown("### 📊 Status")
                st.metric("Round", st.session_state.current_round)
                st.metric("Playing", current_player.name)

            st.markdown("---")
            st.markdown(f"## 🎮 {current_player.name}'s Turn")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 🧰 Available Tools")
                for tool in GameState.TOOLS:
                    suggested = "⭐" if tool.tool in scenario.suggested_tools else ""
                    color = {
                        "Soft Power": "🟦",
                        "Hard Power": "🟥",
                        "Smart Power": "🟩",
                    }.get(tool.power_type.value, "")
                    st.write(
                        f"{suggested} {color} **{tool.tool.value}**: {tool.points_value} pts"
                    )

            with col2:
                st.markdown("### 🎯 Select Your Tools")
                st.markdown("_Choose up to 3 (no duplicates)_")
                selected_tools, selected_indices = [], []
                for i in range(3):
                    available = [t for t in GameState.TOOLS if t not in selected_tools]
                    tool_names = [
                        f"{t.tool.value} ({t.power_type.value})" for t in available
                    ]
                    selected = st.selectbox(
                        f"Tool {i + 1}",
                        options=["None"] + tool_names,
                        key=f"tool_{i}",
                        label_visibility="collapsed",
                    )
                    if selected != "None":
                        selected_tool = available[tool_names.index(selected)]
                        selected_tools.append(selected_tool)
                        selected_indices.append(GameState.TOOLS.index(selected_tool))

            turn_key = f"turn_{st.session_state.current_round}_{st.session_state.current_player_index}"
            if turn_key not in st.session_state:
                st.session_state[turn_key] = False

            if not st.session_state[turn_key]:
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button(
                        "▶️ Play These Tools", key="play", use_container_width=True
                    ):
                        if selected_indices:
                            chosen = [GameState.TOOLS[i] for i in selected_indices]
                            base_pts, syn, var, total = calculate_points(
                                chosen, scenario
                            )
                            current_player.add_round_score(total)
                            if total >= 7:
                                current_player.add_token(scenario.reward_token)
                            st.session_state[turn_key] = True
                            st.rerun()

            if st.session_state[turn_key]:
                chosen = [GameState.TOOLS[i] for i in selected_indices]
                base_pts, syn, var, total = calculate_points(chosen, scenario)

                st.success("✅ **Round Scored!**")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### 📈 Scoring")
                    st.write(f"Base: {base_pts} | Synergy: +{syn} | Variety: +{var}")
                    st.metric("Total", total)

                with col2:
                    st.markdown("### 🛠️ Tools Used")
                    for tool in chosen:
                        badge = {
                            "Soft Power": "🟦",
                            "Hard Power": "🟥",
                            "Smart Power": "🟩",
                        }[tool.power_type.value]
                        st.write(f"{badge} {tool.tool.value}")
                    if total >= 7:
                        st.success(f"🏆 {scenario.reward_token}")

                st.markdown("---")
                st.markdown("### 💭 Reflection")
                prompt = random.choice(st.session_state.reflection_prompts)
                st.write(f"**{prompt}**")
                reflection = st.text_area(
                    "Your thoughts:",
                    key=f"ref_{st.session_state.current_round}_{st.session_state.current_player_index}",
                    height=100,
                    label_visibility="collapsed",
                )

                if st.button("✓ Submit & Continue", use_container_width=True):
                    if reflection:
                        current_player.add_reflection(reflection)
                    st.session_state[turn_key] = False

                    if (
                        st.session_state.current_player_index
                        < len(st.session_state.players) - 1
                    ):
                        st.session_state.current_player_index += 1
                    else:
                        if st.session_state.current_round < st.session_state.max_rounds:
                            st.session_state.current_round += 1
                            st.session_state.current_player_index = 0
                            st.session_state.current_scenario = (
                                st.session_state.scenario_pool.pop(0)
                                if st.session_state.scenario_pool
                                else random.choice(GameState.SCENARIOS)
                            )
                        else:
                            st.session_state.game_over = True
                    st.rerun()


if __name__ == "__main__":
    main()

