def generate_ai_report(patient_name, age, gender, inputs, risk_level, probability):
    """Generates a professional clinical AI assessment report based on patient clinical features."""
    
    # Extract features
    bp = inputs.get("blood_pressure", 120)
    glucose = inputs.get("blood_glucose", 100)
    creatinine = inputs.get("serum_creatinine", 1.0)
    urea = inputs.get("blood_urea", 40)
    albumin = inputs.get("albumin", 0)
    hemoglobin = inputs.get("hemoglobin", 13.5)
    sodium = inputs.get("sodium", 138)
    potassium = inputs.get("potassium", 4.2)
    htn = inputs.get("hypertension", 0)
    diabetes = inputs.get("diabetes", 0)
    smoking = inputs.get("smoking", 0)
    alcohol = inputs.get("alcohol", 0)
    family_hist = inputs.get("family_history", 0)
    
    # Identify key clinical risk factors
    risk_factors = []
    if creatinine > 1.2:
        risk_factors.append(f"Elevated Serum Creatinine ({creatinine} mg/dL) indicating impaired glomerular filtration")
    if albumin > 0:
        risk_factors.append(f"Albuminuria (Grade {albumin}+) indicating glomerular capillary barrier leakage")
    if bp > 130:
        risk_factors.append(f"Systolic/Diastolic Blood Pressure Elevated ({bp} mmHg)")
    if glucose > 125:
        risk_factors.append(f"Hyperglycemia ({glucose} mg/dL) representing potential diabetic nephropathy risk")
    if urea > 45:
        risk_factors.append(f"Elevated Blood Urea Nitrogen ({urea} mg/dL) suggesting nitrogenous waste accumulation")
    if hemoglobin < 12.0:
        risk_factors.append(f"Anemia (Hemoglobin: {hemoglobin} g/dL), often associated with reduced erythropoietin production by kidneys")
    if sodium < 135:
        risk_factors.append(f"Hyponatremia (Sodium: {sodium} mEq/L) - potential electrolyte imbalance")
    if sodium > 145:
        risk_factors.append(f"Hypernatremia (Sodium: {sodium} mEq/L) - sodium retention danger")
    if potassium > 5.0:
        risk_factors.append(f"Hyperkalemia (Potassium: {potassium} mEq/L) - critical cardiovascular risk factor")
    if potassium < 3.5:
        risk_factors.append(f"Hypokalemia (Potassium: {potassium} mEq/L) - electrolyte deficiency")
    if htn:
        risk_factors.append("Pre-existing Systemic Hypertension (accelerates glomerular damage)")
    if diabetes:
        risk_factors.append("Diabetic Mellitus (primary driver of diabetic kidney disease)")
    if smoking:
        risk_factors.append("Active Tobacco Use (associated with renal artery vasoconstriction)")
    if family_hist:
        risk_factors.append("Family History of Renal Failure (genetic susceptibility factor)")

    if not risk_factors:
        risk_factors.append("No major clinical risk factors identified in current values.")
        
    # Interpretations and suggestions based on risk level
    if risk_level == "High Risk":
        interpretation = (
            "Critical clinical signs of renal impairment detected. Glomerular filtration rate is likely "
            "substantially compromised. Accelerated nephron loss and progression toward end-stage renal disease (ESRD) "
            "is highly probable without active clinical intervention. Urgent comprehensive metabolic panel (CMP), "
            "24-hour urine protein check, and specialist review are indicated."
        )
        complications = "Uremic syndrome, Severe hyperkalemia (cardiac arrest risk), Metabolic acidosis, Fluid overload (pulmonary edema, hypertension), Severe anemia, Cardiovascular events."
        lifestyle = "Strictly limit sodium intake (< 1.5g/day). Reduce dietary phosphorus and potassium. Monitor fluid intake. Discontinue NSAIDs."
        diet = "Low protein diet (approx 0.6g/kg/day under dietitian guidance), limited dairy/beans (phosphorus), ban processed meats, avoid high-potassium foods (bananas, potatoes, avocados, spinach)."
        hydration = "Restrict fluid intake strictly to 1.0 - 1.5 liters per day if peripheral edema or oliguria is present. Coordinate with nephrologist."
        follow_up = "Immediate appointment with a board-certified Nephrologist within 24-48 hours. Schedule weekly BP monitoring and monthly blood chemistry panels."
        medication = "Manage BP with ACE inhibitors (e.g. Lisinopril) or ARBs (e.g. Losartan) ONLY under specialist supervision. Avoid nephrotoxic agents (NSAIDs like Ibuprofen, Naproxen, and certain contrast agents)."
        emergency = "Go to the nearest emergency room immediately if experiencing: short of breath (fluid in lungs), chest pain, severe nausea/vomiting, generalized swelling (anasarca), or complete loss of urine output."
        referral = "Urgently refer to Academic Medical Center Nephrology Department."
        
    elif risk_level == "Moderate Risk":
        interpretation = (
            "Mild to moderate kidney risk detected. Potential signs of early-stage Chronic Kidney Disease (CKD Stage 2-3). "
            "Kidneys exhibit early structural or functional changes. Clinical focus must shift to mitigating primary risk "
            "drivers (Hypertension, Diabetes) and protecting remaining nephron function."
        )
        complications = "Progressive renal decline, Mild hypertension, Early-stage anemia, Electrolyte fluctuations."
        lifestyle = "Reduce sodium to < 2.0g/day. Implement regular low-impact aerobic exercise (30 mins/day, 5 days/week). Avoid smoking and limit alcohol."
        diet = "Balanced diet, moderate protein (0.8g/kg/day), rich in whole grains, fresh vegetables, and lean meats. Limit processed items."
        hydration = "Maintain optimal hydration of 2.0 - 2.5 liters of clean water daily unless contraindicated by cardiac conditions."
        follow_up = "Follow up with Primary Care Physician or Nephrologist in 2-4 weeks. Recheck Serum Creatinine and Urine Albumin/Creatinine Ratio (ACR) in 3 months."
        medication = "Strict adherence to prescribed antihypertensives and antidiabetic therapies. Check with pharmacist before starting any over-the-counter painkillers."
        emergency = "Report immediately to clinician if experiencing persistent swelling of hands/feet, unexplained fatigue, dark/foamy urine, or BP reading > 160/100."
        referral = "Recommend consulting a local nephrology clinic for baseline workup."
        
    else: # Low Risk
        interpretation = (
            "Kidney function indicators appear to be within normal clinical ranges. Low probability of current kidney disease. "
            "Focus should remain on preventative health, maintaining blood pressure, and annual physical evaluations."
        )
        complications = "None anticipated; standard age-related decline only."
        lifestyle = "Continue active lifestyle, maintain optimal BMI, healthy diet, and avoid chronic medication abuse."
        diet = "Heart-healthy, balanced diet. Standard sodium intake (< 2.3g/day). Plenty of antioxidant-rich fruits and green vegetables."
        hydration = "Healthy fluid intake of 2.0 - 3.0 liters per day to aid waste excretion."
        follow_up = "Annual routine physical exam with standard urinalysis and metabolic panel."
        medication = "Standard wellness. Avoid unnecessary chronic use of over-the-counter pain relievers."
        emergency = "Standard emergency precautions. Contact physician if sudden urinary changes occur."
        referral = "Standard screening with family physician."

    report = {
        "patient_name": patient_name,
        "age": age,
        "gender": gender,
        "risk_level": risk_level,
        "probability_pct": f"{probability * 100:.1f}%",
        "health_score": f"{100 - (probability * 100):.0f}/100",
        "risk_factors": risk_factors,
        "clinical_interpretation": interpretation,
        "possible_complications": complications,
        "lifestyle_recommendations": lifestyle,
        "diet_suggestions": diet,
        "exercise_suggestions": "30 minutes of moderate-intensity exercise (e.g. brisk walking, cycling) 5 days a week." if risk_level != "High Risk" else "Gentle walking only, avoid high stress strain.",
        "hydration_advice": hydration,
        "follow_up_recommendation": follow_up,
        "medication_reminder": medication,
        "emergency_warning": emergency,
        "hospital_referral_suggestion": referral
    }
    
    return report

def format_ai_report_markdown(report):
    """Formats the generated AI report dict into a beautiful, human-readable markdown text."""
    risk_color = {
        "High Risk": "🔴 **HIGH RISK**",
        "Moderate Risk": "🟡 **MODERATE RISK**",
        "Low Risk": "🟢 **LOW RISK**"
    }.get(report['risk_level'], report['risk_level'])
    
    factors_md = "\n".join([f"- {f}" for f in report['risk_factors']])
    
    md = f"""### Clinical Assessment Report
**Patient Name:** {report['patient_name']}  |  **Age:** {report['age']}  |  **Gender:** {report['gender']}  
**Kidney Health Score:** `{report['health_score']}`  |  **Risk Level:** {risk_color} (`{report['probability_pct']}` probability)

---

#### 🔍 Major Clinical Risk Factors
{factors_md}

#### 📋 Clinical Interpretation
{report['clinical_interpretation']}

#### ⚠️ Possible Complications
{report['possible_complications']}

#### 🥗 Diet & Lifestyle Guidance
* **Lifestyle:** {report['lifestyle_recommendations']}
* **Diet:** {report['diet_suggestions']}
* **Exercise:** {report['exercise_suggestions']}
* **Hydration:** {report['hydration_advice']}

#### 💊 Medical Management
* **Follow-up:** {report['follow_up_recommendation']}
* **Medications:** {report['medication_reminder']}
* **Referral:** {report['hospital_referral_suggestion']}

#### 🚨 Emergency Warnings
> **CRITICAL:** {report['emergency_warning']}
"""
    return md

# Expert Chatbot system logic
def get_chatbot_response(user_query, chat_history_len=0):
    """Parses user queries and returns tailored clinical answers about kidney health."""
    query = user_query.lower().strip()
    
    # 1. Greeting
    if any(k in query for k in ["hello", "hi", "hey", "greetings", "good morning", "good afternoon"]):
        return (
            "Hello! I am **NephroGuard AI**, your dedicated kidney health assistant. "
            "I can help you understand Chronic Kidney Disease (CKD), kidney failure risks, "
            "healthy renal diets, hydration guidelines, and preventative care. How can I assist you today?"
        )
        
    # 2. Diet / Food
    elif any(k in query for k in ["diet", "food", "eat", "nutrition", "protein", "sodium", "salt", "potassium", "phosphorus"]):
        return (
            "### 🥗 Kidney-Healthy Nutritional Guidelines\n\n"
            "For individuals managing kidney health or early stages of CKD, nutrition is vital. Here are the core guidelines:\n\n"
            "1. **Control Sodium (Salt):** High sodium increases blood pressure, which damages kidneys. Keep intake under 2,000 mg/day (about 1 teaspoon of salt). Avoid canned foods, cured meats, and fast foods.\n"
            "2. **Monitor Protein Intake:** Excess protein forces the kidneys to work harder to filter urea. If you have moderate-to-severe CKD, limit protein to **0.6 - 0.8g per kg of body weight** (preferring high-quality lean protein, egg whites, and plant-based protein).\n"
            "3. **Limit High-Potassium Foods (in advanced stages):** Weakened kidneys cannot filter potassium, leading to dangerous heart rhythms. Avoid or limit: bananas, avocados, potatoes, tomatoes, and spinach. Opt for apples, berries, grapes, and cabbage.\n"
            "4. **Manage Phosphorus:** High phosphorus levels draw calcium out of bones, making them weak. Limit dairy products (milk, cheese, yogurt), dark sodas, nuts, and beer.\n\n"
            "*Always consult a registered clinical dietitian for a personalized renal diet plan.*"
        )
        
    # 3. Water / Hydration
    elif any(k in query for k in ["water", "drink", "hydration", "fluid", "how much water", "liquid"]):
        return (
            "### 💧 Hydration and Kidney Health\n\n"
            "Hydration requirements vary dramatically depending on your current kidney function stage:\n\n"
            "- **Healthy Kidneys / Early CKD (Stages 1-2):** Standard hydration (2.0 to 3.0 liters per day) is highly beneficial. It helps the kidneys flush out toxins, urea, and sodium, and reduces the risk of kidney stones.\n"
            "- **Advanced CKD / Kidney Failure (Stages 4-5):** If you experience swelling (edema) in your legs or face, or if urine output is low, your kidneys cannot filter excess fluids. You must restrict fluids (often to **1.0 to 1.5 liters per day**) to prevent fluid accumulation in the lungs and extreme high blood pressure.\n\n"
            "*Tip: To check hydration, monitor your urine color. Pale straw color is ideal. Dark yellow means you need more water.*"
        )
        
    # 4. Symptoms
    elif any(k in query for k in ["symptom", "signs", "how do i know", "pain", "foamy urine", "swelling", "edema", "fatigue"]):
        return (
            "### 🔍 Common Symptoms of Kidney Disease\n\n"
            "Kidneys are highly adaptable, which means Chronic Kidney Disease (CKD) is often a **'silent killer'** with no symptoms until late stages (Stage 4 or 5). Look out for these signs:\n\n"
            "- **Swelling (Edema):** Fluid retention causing puffiness around the eyes, or swelling in the feet, ankles, and hands.\n"
            "- **Changes in Urination:** Urinating more frequently (especially at night), dark or tea-colored urine, or highly foamy/bubbly urine (indicating protein leakage).\n"
            "- **Persistent Fatigue & Brain Fog:** Caused by buildup of toxins in the blood or anemia (low red blood cells due to reduced erythropoietin hormone).\n"
            "- **Shortness of Breath:** Excess fluid building up in the lungs.\n"
            "- **Metallic Taste in Mouth / Ammonia Breath:** Due to urea buildup (uremia).\n"
            "- **Nausea, Vomiting, and Loss of Appetite.**\n"
            "- **Dry, Itchy Skin:** Caused by mineral and hormone imbalances in the blood."
        )
        
    # 5. Prevention / Healthy lifestyle
    elif any(k in query for k in ["prevent", "avoid", "protect", "lifestyle", "exercise", "smoking", "alcohol"]):
        return (
            "### 🛡️ How to Prevent and Slow Kidney Decline\n\n"
            "Whether you have healthy kidneys or early-stage kidney disease, these preventive strategies protect your nephrons:\n\n"
            "1. **Manage Blood Pressure:** Keep BP below **130/80 mmHg**. Hypertension is the second leading cause of kidney failure.\n"
            "2. **Control Blood Sugar:** If you have diabetes, keep HbA1c in check. Diabetic nephropathy is the leading cause of renal failure worldwide.\n"
            "3. **Avoid Overuse of NSAIDs:** Over-the-counter painkillers like **Ibuprofen (Advil, Motrin), Naproxen (Aleve)**, and high-dose Aspirin are nephrotoxic and reduce blood flow to the kidneys. Use Acetaminophen (Tylenol) instead.\n"
            "4. **Exercise regularly:** 30 minutes of moderate activity (brisk walking, swimming) daily lowers BP and blood glucose.\n"
            "5. **Quit Smoking:** Smoking damages blood vessels and speeds up renal function decline.\n"
            "6. **Annual Screening:** Ask your doctor for an annual **eGFR (blood test)** and **Urine ACR (protein urinalysis)**."
        )
        
    # 6. Emergency / High risk
    elif any(k in query for k in ["emergency", "critical", "severe", "danger", "chest pain", "shortness of breath", "esrd", "dialysis"]):
        return (
            "### 🚨 Emergency Clinical Warning Signs\n\n"
            "If you or a patient have advanced kidney failure, you must monitor for **uremic emergencies** and severe fluid overload. **Go to the ER immediately if you experience:**\n\n"
            "- **Severe fluid buildup:** Difficulty breathing or crackling sounds in the lungs, even when lying flat.\n"
            "- **Cardiac issues:** Chest pain, chest pressure, or irregular heartbeats (often caused by high potassium/hyperkalemia).\n"
            "- **Severe Neurological symptoms:** Seizures, confusion, extreme drowsiness, or loss of consciousness.\n"
            "- **Severe Gastrointestinal distress:** Constant vomiting, inability to keep food/liquids down, and complete loss of strength."
        )
        
    # 7. Creatinine / Urea / Albumin explanation
    elif any(k in query for k in ["creatinine", "urea", "albumin", "gfr", "egfr", "blood pressure"]):
        return (
            "### 🧪 Understanding Your Kidney Lab Results\n\n"
            "- **Serum Creatinine:** A waste product from muscle breakdown. Healthy kidneys filter it completely. Normal ranges are **0.6 to 1.2 mg/dL**. If it rises, it means kidney filtration is decreasing.\n"
            "- **Blood Urea Nitrogen (BUN) / Blood Urea:** A waste product from protein digestion. Normal is **7 to 20 mg/dL** (urea around **15 to 45 mg/dL**). Elevated levels indicate waste accumulation.\n"
            "- **Microalbumin / Albumin:** A key protein in the blood. Healthy kidneys keep it in the blood. Albumin in urine (proteinuria) means the kidney's filter system is leaking. Normal is **Grade 0**. Grade 1+ to 5+ indicates progressive kidney damage.\n"
            "- **eGFR (Estimated Glomerular Filtration Rate):** The best measure of kidney function. Above 90 is normal. Below 60 for 3+ months indicates Chronic Kidney Disease. Below 15 indicates kidney failure (requiring dialysis or transplant)."
        )
        
    # 8. Default
    else:
        return (
            "I apologize, I didn't quite catch the specifics of your request. "
            "Please ask me about:\n"
            "- **Kidney-healthy diets** (limiting sodium, potassium, phosphorus, protein)\n"
            "- **Water intake guidelines** and fluid restrictions\n"
            "- **Symptoms** of Chronic Kidney Disease (CKD)\n"
            "- **Lab tests** (Serum Creatinine, Blood Urea, Albumin, eGFR)\n"
            "- **Preventing kidney decline** (NSAIDs, blood pressure, diabetes control)\n"
            "- **Emergency warning signs** indicating urgent care needs"
        )
