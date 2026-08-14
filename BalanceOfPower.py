# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "plotly==6.9.0",
# ]
# ///

import marimo

__generated_with = "0.18.3"
app = marimo.App(width="medium")

with app.setup:
    # Initialization code that runs before all other cells
    pass


@app.cell
def _():
    return


@app.cell
def _():
    import marimo as mo
    import plotly.graph_objects as go
    import math

    __generated_with = "0.1.0"
    app = mo.App(width="full")
    return go, math, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Riding the Heatweave: The Balance of Power
    This is the first part of a series of three articles about cycling in a world of increasing heatwaves and global warming. We look at the physics of heat loss.
    """)
    return


@app.cell
def _(mo):
    _src = (
        "AridCyclist_20260812_114639.png"
    )
    mo.image(src=_src, width="360px", height="360px", rounded=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Thermodynamics of Cycling in the Heat
    When you look down at your power meter and see 280 W, it is telling you the rate at which your legs are transferring energy into the drivechain to overcome rolling resistance, gravity and aerodynamic drag. However this is just a fraction of power that your body is generating. Muscles are only 20% to 25% efficient at converting chemical energy (think ATP) into mechanical energy. The rest of the effort is wasted in the form of internal heat. <br>
    Riding at 280 W, your body is producing excess heat equivalent to a 1 kW electric heater. Heatstroke occurs when body temperature exceeds $40^\circ\text{C}$. Under severe heat stress, proteins start to unfold and stick together like a poached egg. To prevent your core temperature from soaring into dangerous territory, your body must continuously dissipate high thermal loads into the surrounding environment.<br>
    There are three ways for the body to lose heat:
    - the flow of cooler air over the skin
    - the body continuously emits infra-red radiation into the environment
    - evaporation of sweat
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Power Balance Equation
    In classical environmental physiology, human thermoregulation is described by the Heat Balance Equation, which tracks total thermal energy ($S$) stored in human tissue over time. Because cyclists quantify effort in Watts (Joules per second, or $\text{J/s}$), we can divide every term in the traditional heat balance equation by time. This converts the thermodynamic balance sheet directly into a Power Balance Equation:<br>$P_{\text{storage}} = P_{\text{heat}} -  P_{\text{conv}} - P_{\text{rad}} - P_{\text{evap}}$ <br>
    Where every term is expressed in Watts ($W$):
    - $P_{\text{storage}}$ (Net Thermal Storage Power): The rate at which heat is accumulating in your body. If $P_{\text{storage}} = 0$, you are in thermal equilibrium. If $P_{\text{storage}} > 0$, your core body temperature is rising.
    - $P_{\text{heat}}$ (Internal Heat Production): Rate of production of heat in the muscles as a result of producing mechanical power. This is the total rate of chemical energy expenditure by your body $P_{\text{met}}$ minus the mechanical work output measured by your bike's power meter $P_{\text{mech}}$.
        -  $P_{\text{heat}} = P_{\text{met}}  - P_{\text{mech}}$
    - $P_{\text{conv}}$ (Convective Power Transfer): Rate of thermal energy lost (or gained) via airflow moving across your skin.
    - $P_{\text{rad}}$ (Radiative Power Transfer): Rate of thermal energy exchanged between body and environment (sunlight, air and ground heat) via electromagnetic radiation. Direct sunlight can have a significant warming effect.
    - $P_{\text{evap}}$ (Evaporative Power Loss): Rate of thermal energy dissipated through sweat evaporation
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Knowledge is Power
    You can use this interactive tool to gain valuable insights from the Power Balance Equation that can help you cope with riding during a heatwave.
    """)
    return


@app.cell
def _(mo):
    def ui_sliders(mo):
        # Setup interactive sliders for the widget
        weight = mo.ui.slider(start=45, stop=100, step=1, value=70, label="Weight (kg)")
        height = mo.ui.slider(start=1.50, stop=2.00, step=0.01, value=1.78, label="Height (m)")
        power = mo.ui.slider(start=0, stop=500, step=10, value=250, label="Mechanical Power (W)")

        speed = mo.ui.slider(start=0, stop=60, step=1, value=25, label="Air Speed (km/h)")
        temp = mo.ui.slider(start=25, stop=45, step=1, value=32, label="Ambient Temp (°C)")
        humidity = mo.ui.slider(start=10, stop=100, step=5, value=60, label="Rel. Humidity (%)")
        sunny = mo.ui.switch(label="Direct sunlight")
        return height, humidity, power, speed, temp, weight, sunny
    height, humidity, power, speed, temp, weight, sunny = ui_sliders(mo)
    return height, humidity, power, speed, sunny, temp, weight


@app.cell
def _(math, sunny):
    def physics_engine(height, humidity, power, speed, temp, weight):
        # 1. Physical & Physiological Constants
        eta = 0.22  # 22% Gross mechanical efficiency
        T_s = 34.0  # Skin temperature approx (°C)

        m = weight.value
        h = height.value
        P_mech = power.value
        v_ms = speed.value / 3.6  # km/h to m/s
        T_a = temp.value
        RH = humidity.value

        # 2. Body Surface Area (Du Bois formula, height in meters)
        BSA = 0.20247 * (m ** 0.425) * (h ** 0.725)

        # 3. Internal Heat Generation (Watts)
        P_heat = P_mech * ((1 - eta) / eta)

        # 4. Convective Cooling
        h_c = 5.8 * (v_ms ** 0.8)
        P_conv = h_c * BSA * (T_s - T_a)

        # 5. Radiative Cooling
        h_r = 6.0
        eff = 0.72
        T_sun = 30 * sunny.value
        P_rad = h_r * BSA * 0.72 * (T_s - (T_a + T_sun))

        # 6. Evaporative Cooling Potential (Tetens Equation)
        def P_sat(T):
            return 0.61078 * math.exp((17.27 * T) / (T + 237.3))

        P_sk_s = P_sat(T_s)
        P_a = (RH / 100) * P_sat(T_a)

        h_e = 16.5 * h_c
        P_evap_max = h_e * BSA * max(0, P_sk_s - P_a)

        # 7. Net Balance & Storage
        # Only sweat as much as needed to maintain 0 storage, up to the max capacity
        P_evap_req = max(0, P_heat - P_conv - P_rad)
        P_evap = min(P_evap_req, P_evap_max)

        P_storage = P_heat - P_conv - P_rad - P_evap

        # 8. Core Temperature Drift Rate (°C / hr)
        dTc_dt = (P_storage * 3600) / (m * 3490)

        return BSA, P_conv, P_evap, P_evap_max, P_evap_req, P_heat, P_rad, P_storage, dTc_dt
    return (physics_engine,)


@app.cell
def _(go, height, humidity, physics_engine, power, speed, temp, weight):

    BSA, P_conv, P_evap, P_evap_max, P_evap_req, P_heat, P_rad, P_storage, dTc_dt = physics_engine(height, humidity, power, speed, temp, weight)
    # Constructing the Plotly Waterfall Chart
    fig = go.Figure(go.Waterfall(
        name="Power Balance", 
        orientation="v",
        measure=["relative", "relative", "relative", "relative", "total"],
        x=["Internal Heat", "Convection", "Radiation", "Evaporation", "Net Heat Storage"],
        textposition="outside",
        # Flip signs for display so negative values accurately subtract from the stack
        text=[
            f"+{int(P_heat)} W", 
            f"{-int(P_conv)} W", 
            f"{-int(P_rad)} W", 
            f"{-int(P_evap)} W", 
            f"{int(P_storage)} W"
        ],
        y=[P_heat, -P_conv, -P_rad, -P_evap, P_storage],
        decreasing={"marker": {"color": "#3b82f6"}}, # Blue for cooling
        increasing={"marker": {"color": "#ef4444"}}, # Red for heating
        totals={"marker": {"color": "#8b5cf6"}},     # Purple for net accumulation
        connector={"line": {"color": "rgb(63, 63, 63)", "width": 1}}
    ))

    # Color formatting for the title based on heat danger
    status_color = "red" if dTc_dt > 0.5 else ("orange" if dTc_dt > 0 else "green")
    time2heatstroke = f"**Time to heatstroke: {3/dTc_dt*60:.0f} mins**" if dTc_dt>0 else ""
    fig.update_layout(
        title=f"<b>Thermodynamic Power Balance: Cycling at {power.value}W airspeed {speed.value}km/h in {temp.value}°C humidity {humidity.value}%</b><br>"
              f"<span style='color:{status_color}'>Core Temp Drift: {dTc_dt:+.1f} °C/hr {time2heatstroke}</span>"       
              f"  | <span style='color:gray'>Evaporative Ceiling: {int(P_evap_max)} W</span>",
        showlegend=False,
        yaxis_title="Power (Watts)",
        waterfallgap=0.3,
        margin=dict(t=80, b=40, l=60, r=40)
    )

    fig.update_yaxes(range=[-1000, 2000], zeroline=True, zerolinecolor='green', zerolinewidth=2)
    return P_evap, P_evap_max


@app.cell
def _(
    P_evap,
    P_evap_max,
    height,
    humidity,
    mo,
    power,
    speed,
    sunny,
    temp,
    weight,
):
    # Provide visual feedback on sweating efficiency
    sweat_status = ""
    if P_evap >= P_evap_max and P_evap_max > 0:
        sweat_status = "⚠️ **Warning:** Evaporation is maxed out. Excess sweat will drip off and waste fluid without cooling."

    # Assemble the final UI grid
    controls = mo.hstack(
        [
            mo.vstack(
                [
                    mo.md("### 🚴 Cycling Inputs"),
                    power, speed

                ]
            ),
            mo.vstack(
                [
                    mo.hstack([mo.md("### 🌤️ Environment"),sunny]),
                    temp, humidity,
                    mo.md(sweat_status)
                ]
            ),
            mo.vstack(
                [
                    mo.md("### 🚴🏽‍♂️ Rider Inputs"),
                    weight, height
                ]
            ),

        ],
        gap=1,
    )
    controls
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - The bar on the left shows the rate of production of internal heat. The next three bars show how the body attempts to dissipate excess heat through convection, radiation and evaporation. Red is heating and blue is cooling. Any remaining imbalance affects the body's core temperatue at the rate shown in the Net Heat Storage bar on the far right hand side.
    - Start by adjusting the weight and height sliders on the right to match your stature. These are used to estmate your body surface area, which relates to heat loss.
    - Ajusting the slider for Mechanical Power (the figure displayed on your power meter) drives the amount of Internal Heat generated by the muscles. This heat is the energy lost in the conversion of chemical energy into mechanical energy. As you push harder on the pedals, your body generates more internal heat. This needs to be lost to the environment in order to maintain a steady core body temperature.
    - Changing the Airspeed affects convection and evaporation. Airspeed is primarily determined by the speed you are riding your bike, but it also changes if there is a strong wind blowing. Cycling has a great advantage over running and other sports in creating its own airflow. The cooling effect of the apparent wind leaves cyclists less exposed to the risk of overheating in hot weather. However this benefit falls when riding uphill with the same power but at a lower speeds (move the slider to the left). If you reduce Airspeed to zero, you see how important it is to use a fan and keep the room cool when riding on an indoor turbo. In a hot, humid room with no airflow, you body can overheat quickly.
    - Toggle the direct sunlight button to see the significant radiative warming effect of moving from shade/cloud cover into direct sunlight. On a clear sunny day at noon this can raise the effective ambient temperature by a staggering $30^\circ\text{C}$, so your body gains rather than losing heat. I was grateful to be climbing under tree cover in the Atlantic Pyrenees earlier this summer.
    - The effects of rising Ambient Temperature are the key focus of this analysis. In the shade, your body can lose heat if your skin is warmer than the environment. By moving the slider to the right, you see that when heatwave temperatures exceed skin temperature (set at $34^\circ\text{C}$ for this model), convection and radiation can no longer cool the body. In fact they switch to warming the body. Evaporation becomes the only remaining means of heat loss.
    - The Relative Humidity slider puts a ceiling on the rate of evaporation (shown at the top of the chart). In very hot humid conditions, sweat cannot evaporate and rolls off the skin without providing any cooling effect. In damper regions relative humidity tends to be over 60%, while in arid areas it may be below 30%. The historic average for the Tour de France in July is <a href="https://www.worlddata.info/europe/france/climate.php">74%</a>. Global humidity is on a rising trend around the world.
    - When the body is able to dissipate excess heat, Net Heat Storage is zero and core body temperature remains stable (thermal homeostasis). However, when the body is unable to dump excess heat, core body temperature starts to rise. Normal body temperature is $37.4^\circ\text{C}$ and an increase of $3^\circ$ can cause the symptoms of heatstroke: fatigue, diziness, headache, nausea etc.. When the Net Heat Storage is positive, the model estimates how long it will take for heatstroke to occur, if power is maintained under the prevailing ambient conditions.
    - It is possible for Net Heat Storage to become negative, even in hot weather. For example, if you stop pedalling (set Mechanical Power to zero) while freewheeling down a hill at 60km/h in $30^\circ\text{C}$ on a cloudy day, you lose heat from the convective airflow over your skin (and most likely some more from the evaporation of sweat produced during the prior ascent). This is why it is helpful to put on a gilet (or stuff a copy of Gazzetta dello Sport down the front of your jersey) as you crest the Stelvio. The cooling effect is probably less than the model suggests, because temperates are higher at lower altitudes - it's warmer in the valleys than on the summits.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Is the world becomes warmer, more of us will need to apt to riding the heatwaves. The next in article this series explores the physiological changes that occur when you encounter a hot environment.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Technical Appendix: Breakdown of the Balance of Power Equation

    ### Step 1: Internal Heat Production ($P_{\text{heat}}$)
    The total metabolic power expended by your body ($P_{\text{met}}$) depends on mechanical power output ($P_{\text{mech}}$) and gross efficiency ($\eta \approx 0.22$):<br>$P_{\text{met}} = \frac{P_{\text{mech}}}{\eta}$<br>The rate of internal thermal power generated by working muscles ($P_{\text{heat}}$) is the difference between total metabolic power and mechanical power pushed to the pedals:<br>$P_{\text{heat}} = P_{\text{met}} - P_{\text{mech}} = P_{\text{mech}} \times \left(\frac{1 - \eta}{\eta}\right)$<br>
    ### Step 2: Convective Heat Transfer ($P_{\text{conv}}$)
    Convective cooling occurs as moving air carries thermal energy away from exposed skin. Modern Computational Fluid Dynamics research on cyclists by <a href="https://europepmc.org/article/MED/21497817">Defaeye (2011)</a> demonstrates that highly turbulent airflow yields a power-law exponent estimate of  heat transfer coefficient ($h_c$) that scales non-linearly with air velocity ($v$ in $\text{m/s}$):<br>$h_c = 5.8 \times v^{0.8} \quad [\text{W/(m}^2\cdot^\circ\text{C)}]$<br>The total convective power exchange is:<br>$P_{\text{conv}} = h_c \times BSA \times (T_s - T_a)$<br>$BSA$: Body Surface Area can be estimated from height and weight (Du Bois formula)<br>$T_s$: Skin temperature<br>$T_a$: Ambient temperature of the air<br>
    - Cool/Warm Air ($T_a < T_s$): $P_{\text{conv}}$ is positive—air cools the skin.
    - Extreme Heat ($T_a > T_s$): $P_{\text{conv}}$ becomes negative—air actually heats the body, adding to the thermal load.
    ### Step 3: Radiative Heat Transfer ($P_{\text{rad}}$)
    Radiative heat loss is driven by the temperature difference between skin and surrounding air, surfaces and sunlight. It is estimated using a linearized radiative heat transfer coefficient ($h_r \approx 6.0 \text{ W/(m}^2\cdot^\circ\text{C)}$) with an effective area of between 70% and 75% of body surface. Exposure to direct sunlight versus shade has a signficant impact.<br>$P_{\text{rad}} = h_r \times (BSA \times 0.72) \times (T_s - (T_a + T_{sun}))$<br>where $T_{sun} = 0^\circ\text{C}$ in shade and $30^\circ\text{C}$ in direct sunlight, representing a clear summer day at noon.
    ### Step 4: Evaporative Potential ($P_{\text{evap, max}}$) and Humidity
    When ambient temperature exceeds skin temperature ($T_a > T_s$), convection and radiation can no longer cool the body. Evaporation becomes the only remaining avenue for heat loss. <br>Evaporation is governed by the difference in water vapor pressure between wet skin $P_{sk,s} = P_{sat}(T_s)$ and the air, which are derived from the <a href="https://en.wikipedia.org/wiki/Tetens_equation">Tetens Equation</a> and adjusting for the relative humidity of the air.<br>$P_a = \left(\frac{RH}{100}\right) \times P_{sat}(T_a)$<br>The amount of evaporative heat loss depends on a heat transfer coefficient linked to airflow.
    Using the Lewis Relation for heat and mass transfer, the evaporative heat transfer coefficient ($h_e$) is directly tied to the convective wind coefficient ($h_c$):<br>$h_e = 16.5 \times h_c \quad (\text{in W/m}^2\cdot\text{kPa})$<br>
    Maximum Evaporative Potential ($P_{\text{evap, max}}$ ) represents the absolute physiological ceiling of how much heat the environment can evaporate from the athlete's body surface area ($BSA$):<br>$P_{\text{evap, max}}  = h_e \times BSA \times (P_{sk,s} - P_a)$.
    This declines (potentially to zero) in very hot and humid conditions.<br>
    The body's Required Evaporative Cooling ($P_{\text{evap, req}}$) to maintain stable core temperature is whatever internal heat reaches the skin that wasn't cleared by convection or radiation:<br>$P_{\text{evap, req}} = P_{\text{heat}} - (P_{\text{conv}} + P_{\text{rad}})$<br>Actual evaporative heat loss ($P_{\text{evap}}$) cannot exceed $P_{\text{evap, max}}$:<br>$P_{\text{evap}} = \min(P_{\text{evap, req}}, P_{\text{evap, max}})$<br>If $P_{\text{evap, req}} > P_{\text{evap, max}}$, the skin cannot evaporate all the sweat produced. Extra sweat drips off uselessly (wasted sweat), while unevaporated thermal energy is trapped inside the body.
    ### Step 5: Thermal Storage ($P_{\text{storage}}$) and Core Temperature Drift
    Summing all dissipation channels gives the net power accumulating in tissue:<br>$P_{\text{storage}} = P_{\text{heat}} - (P_{\text{conv}} + P_{\text{rad}} + P_{\text{evap}})$<br>This can be converted into an hourly rate of core temperature change, taking account of the specific heat capacity of human tissue.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Source code for this project at https://github.com/science4performance/RidingTheHeatwave
    """)
    return


if __name__ == "__main__":
    app.run()
