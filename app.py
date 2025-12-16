import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# -----------------------------
# Page Config & The Hook
# -----------------------------
st.set_page_config(page_title="Case 11: The Shaky Bridge Mystery", page_icon="🌉", layout="wide")

st.title("🌉 Case 11: The Shaky Bridge Mystery")
st.markdown("""
**Case File:** Inspector Watson! We have a delicate case on our hands.
The inspector on the bridge is unable to adapt to the changing conditions (rust, storm, heavy load).

**Holmes's Command:**
*"I don't just want a system that works, I want you to find the **most elegant balance** for me."*
Manage that delicate 'tension' between speed and safety. And remember, every decision has a price.
""")
st.markdown("---")

# -----------------------------
# 1. Sidebar - "Examine the Evidence" (Sharpen the Mystery)
# -----------------------------
st.sidebar.header("🕵️‍♂️ Evidence Files")

# Scenario Selection -> Evidence Review
evidence = st.sidebar.radio(
    "Which clue will you follow?",
    ["File A: Blue Copy (Reference)",
     "File B: Truck Load Report (Heavy Load)",
     "File C: Maintenance Records (Corrosion)",
     "File D: Weather Report (Storm)"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("🎛️ Control Room")

Kp = st.sidebar.slider(
    "Intervention Force (Kp)",
    0.0, 50.0, 10.0, 1.0,
    help="How harshly are we intervening in the system?"
)

# Engineering Stress (Visualize the Trade-off)
# Simple visualization: As Kp increases, Speed increases, Security decreases.
st.sidebar.caption("⚖️ **Engineering Tension**")
st.sidebar.progress(min(Kp/50.0, 1.0))
c1, c2 = st.sidebar.columns(2)
c1.markdown("<small>🐢 Stability</small>", unsafe_allow_html=True)
c2.markdown("<small style='float:right'>⚡ Speed /Risk</small>", unsafe_allow_html=True)


# -----------------------------
# 2. Physics & Contextual Anchoring
# -----------------------------
# Nominal Parameters
m_nom, c_nom, k_nom, x_ref = 2.0, 0.8, 10.0, 1.0

# Visual Metaphors
def get_load_context(alpha):
    if alpha <= 1.0: return "🐎 Light Carriage", "blue"
    if alpha <= 1.6: return "🚛 Steam Truck", "orange"
    return "🚂 Freight Train (Overloaded)", "red"

def get_rust_context(alpha):
    if alpha >= 1.0: return "✨ Brand New Metal", "blue"
    if alpha >= 0.5: return "🔩 Squeaky Joints", "orange"
    return "☠️ Rotten Metal", "red"

# Parameters According to the Evidence File
alpha_m, alpha_c = 1.0, 1.0

# FIX: "is in" -> "in"
if "File A" in evidence:
    st.sidebar.info("Mode: Calibration (Theory)")

elif "File B" in evidence:
    alpha_m = st.sidebar.slider("Load Status", 1.0, 2.0, 1.5)
    icon, color = get_load_context(alpha_m)
    st.sidebar.markdown(f"**Load:** :{color}[{icon}]")

elif "File C" in evidence:
    alpha_c = st.sidebar.slider("Metal Health", 0.0, 2.0, 0.5)
    icon, color = get_rust_context(alpha_c)
    st.sidebar.markdown(f"**Status:** :{color}[{icon}]")

else: # Storm (File D)
    alpha_m = st.sidebar.slider("Load", 0.5, 2.5, 1.4)
    alpha_c = st.sidebar.slider("Metal", 0.0, 2.0, 0.6)

m_true = alpha_m * m_nom
c_true = alpha_c * c_nom

# -----------------------------
# 3. Simulation Engine
# -----------------------------
def simulate_bridge(m, c, k, Kp, x_target, t_max=15.0, dt=0.01):
    n_steps = int(t_max / dt)
    t = np.linspace(0, t_max, n_steps)
    x = np.zeros(n_steps)
    v = np.zeros(n_steps)
    # FIX: np.zero -> np.zeros
    u = np.zeros(n_steps)
    
    for i in range(n_steps - 1):
        u[i] = Kp * (x_target - x[i])
        a = (-c * v[i] - k * x[i] + u[i]) / m
        v[i+1] = v[i] + a * dt
        x[i+1] = x[i] + v[i] * dt
        
    return t, x, u

t, x_nom, u_nom = simulate_bridge(m_nom, c_nom, k_nom, Kp, x_ref)
t, x_true, u_true = simulate_bridge(m_true, c_true, k_nom, Kp, x_ref)

# -----------------------------
# 4. Analysis & Dynamic Feedback (Embed the Context)
# -----------------------------
def get_metrics(x_arr, t_arr, target):
    max_val = np.max(x_arr)
    overshoot = max(0, (max_val - target) / target) * 100
    tol = 0.05 * target
    settling_time = t_arr[-1]
    for i in range(len(x_arr)-1, 0, -1):
        if abs(x_arr[i] - target) > tol:
            settling_time = t_arr[i]
            break
    return overshoot, settling_time

os_true, ts_true = get_metrics(x_true, t, x_ref)
os_nom, ts_nom = get_metrics(x_nom, t, x_ref)
u_cost = np.sum(np.abs(u_true)) * 0.1 # Cost Simulation (£)

# Feedback Logic
holmes_feedback = []
status_bg = "#f0f2f6"

# A. Overshoot -> Airplane Analogy
if os_true > 30.0:
    holmes_feedback.append({
        "icon": "✈️",
        "title": "TURBULENCE WARNING",
        "msg": "This oscillation is like a plane shaking its passengers in a storm. Fast but dangerous.",
        "type": "error"
    })
    status_bg = "#ffeeee"

# B. Settling Time -> Car Analogy
elif ts_true > 10.0:
    holmes_feedback.append({
        "icon": "🚗",
        "title": "CAR STUCK ON THE HILL",
        "msg": "The system behaves like a car with a full trunk stalling on a hill. Safe but dysfunctional.",
        "type": "warning"
    })
    status_bg = "#fff8e1"

# C. High Cost (Control Effort) -> Budget Alert
if u_cost > 500:
    holmes_feedback.append({
        "icon": "💸",
        "title": "BUDGET OVERLOAD",
        "msg": f"Monthly energy bill has risen to £{u_cost:.0f}! Scotland Yard does not approve of this.",
        "type": "warning"
    })

# D. Success (Elegance)
if not holmes_feedback and os_true < 15.0:
    holmes_feedback.append({
        "icon": "🦢",
        "title": "ELEGANT SOLUTION",
        "msg": f"Perfect balance! Both safe and economical (£{u_cost:.0f}). A real detective job.",
        "type": "success"
    })
    status_bg = "#e8f5e9"

# -----------------------------
# 5. Visualization & Report
# -----------------------------
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Blue Copy vs. Rusty Reality")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_facecolor(status_bg)
    
    ax.plot(t, x_nom, 'b--', alpha=0.5, label="Theory")
    ax.plot(t, x_true, 'r-', linewidth=2.5, label="True")
    ax.axhline(x_ref, color='k', linestyle=':', label="Target")
    
    # Contextual Icons on Graph
    if os_true > 30.0:
        ax.text(t[np.argmax(x_true)], np.max(x_true), "✈️", fontsize=20)
    if ts_true > 10.0:
        ax.text(ts_true, x_true[-1], "🚗", fontsize=20)
        
    ax.set_ylabel("Stretch (m)")
    ax.legend()
    st.pyplot(fig)

with col2:
    st.subheader("📝 Holmes's Deductions")
    
    for fb in holmes_feedback:
        if fb["type"] == "error": st.error(f"**{fb['icon']} {fb['title']}**\n\n{fb['msg']}")
        elif fb["type"] == "warning": st.warning(f"**{fb['icon']} {fb['title']}**\n\n{fb['msg']}")
        elif fb["type"] == "success": st.success(f"**{fb['icon']} {fb['title']}**\n\n{fb['msg']}"); st.balloons()
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    c1.metric("Excessive Oscillation", f"{os_true:.1f}%")
    c2.metric("Operating Cost", f"£{u_cost:.0f}")

# -----------------------------
# 6. Case Report (Synthesis - Pro/Con)
# -----------------------------
st.markdown("---")
with st.expander("📂 Case Report: Evidence for and Against", expanded=True):
    st.markdown("### Decision Analysis")
    
    # Dynamic Synthesis
    pros = []
    cons = []
    
    if os_true < 10.0: 
        pros.append("✅ Low Oscillation: Structural integrity is preserved.")
    else: 
        cons.append(f"❌ High Risk: %{os_true:.1f} emissions create metal fatigue.")
    
    # FIX: Logic was missing here
    if ts_true < 5.0: 
        pros.append("✅ Quick Response: Traffic flow was not interrupted.")
    else: 
        cons.append("❌ Sluggish Response: The system is responding with a delay.")
    
    # FIX: Logic was corrupted here
    if u_cost < 300: 
        pros.append("✅ Economic: Budget-friendly operation.")
    else: 
        cons.append("❌ Expensive: High energy consumption.")
    
    col_pro, col_con = st.columns(2)
    with col_pro:
        st.markdown("**FAVORABLE (Advantages)**")
        for p in pros: st.write(p)
    with col_con:
        st.markdown("**ADVERSITY (Disadvantages)**")
        for c in cons: st.write(c)