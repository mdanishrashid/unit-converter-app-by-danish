import streamlit as st
from pint import UnitRegistry

# Initialize Unit Registry
ureg = UnitRegistry()
ureg.define("square_meter = meter ** 2")
ureg.define("square_kilometer = kilometer ** 2")
ureg.define("square_mile = mile ** 2")
ureg.define("square_yard = yard ** 2")
ureg.define("square_foot = foot ** 2")
ureg.define("square_inch = inch ** 2")
ureg.define("hectare = 10000 * meter ** 2")
ureg.define("acre = 4046.86 * meter ** 2")

def convert_units(value, from_unit, to_unit):
    try:
        if from_unit in ["celsius", "fahrenheit", "kelvin"] and to_unit in ["celsius", "fahrenheit", "kelvin"]:
            result = ureg.Quantity(value, ureg(from_unit)).to(ureg(to_unit))
        else:
            result = (value * ureg.parse_expression(from_unit)).to(ureg.parse_expression(to_unit))
        return result.magnitude
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("Unit Converter App by Danish")
    
    unit_categories = {
        "Length": ["meter", "kilometer", "mile", "yard", "foot", "inch", "centimeter", "millimeter"],
        "Weight": ["gram", "kilogram", "pound", "ounce", "ton"],
        "Temperature": ["celsius", "fahrenheit", "kelvin"],
        "Volume": ["liter", "milliliter", "gallon", "quart", "pint", "cup", "fluid_ounce"],
        "Area": ["square_meter", "square_kilometer", "square_mile", "square_yard", "square_foot", "square_inch", "hectare", "acre"],
        "Speed": ["meter_per_second", "kilometer_per_hour", "mile_per_hour", "foot_per_second", "knot"],
        "Time": ["second", "minute", "hour", "day", "week", "month", "year"],
        "Energy": ["joule", "calorie", "kilojoule", "kilocalorie", "watt_hour", "electronvolt"],
        "Power": ["watt", "kilowatt", "horsepower", "megawatt"],
        "Pressure": ["pascal", "bar", "atm", "torr", "psi"]
    }
    
    category = st.selectbox("Select a category", list(unit_categories.keys()))
    
    if "from_unit" not in st.session_state or "to_unit" not in st.session_state:
        st.session_state.from_unit = unit_categories[category][0]
        st.session_state.to_unit = unit_categories[category][1]
    
    st.session_state.from_unit = st.selectbox("From Unit", unit_categories[category],
                                              index=unit_categories[category].index(st.session_state.from_unit) 
                                              if st.session_state.from_unit in unit_categories[category] else 0)
    
    st.session_state.to_unit = st.selectbox("To Unit", unit_categories[category],
                                            index=unit_categories[category].index(st.session_state.to_unit) 
                                            if st.session_state.to_unit in unit_categories[category] else 1)
    
    if st.button("Swap Units 🔄"):
        st.session_state.from_unit, st.session_state.to_unit = st.session_state.to_unit, st.session_state.from_unit
        st.rerun()
    
    value = st.number_input("Enter value", min_value=0.0, format="%f")
    
    if st.button("Convert"):
        result = convert_units(value, st.session_state.from_unit, st.session_state.to_unit)
        st.success(f"{value} {st.session_state.from_unit} = {result} {st.session_state.to_unit}")

if __name__ == "__main__":
    main()

