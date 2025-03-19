import streamlit as st #test
import re
from fractions import Fraction

def convert_mixed_to_improper(whole, num, den):
    return (whole * den + num, den)

def simplify_fraction(num, den):
    if den == 0:
        return "Undefined"  # Avoid zero denominator
    if num == 0:
        return "0/1"
    common = Fraction(num, den)
    return f"{common.numerator}/{common.denominator}"

def compute_correct_answer(f1, f2, op):
    n1, d1 = f1
    n2, d2 = f2
    if op == '+':
        return simplify_fraction(n1 * d2 + n2 * d1, d1 * d2)
    elif op == '-':
        return simplify_fraction(n1 * d2 - n2 * d1, d1 * d2)
    elif op == '×':
        return simplify_fraction(n1 * n2, d1 * d2)
    else:  # Division
        return simplify_fraction(n1 * d2, d1 * n2)

def classify_error(user_input, correct_answer):
    n1, d1, op, n2, d2, user_num, user_den = user_input
    correct_num, correct_den = map(int, correct_answer.split('/'))
    
    errors = {
        "resp_err_c-a": simplify_fraction(n1 + d1, d2),
        "resp_err_c-b": simplify_fraction(n1, d1 + d2),
        "resp_err_c-c": simplify_fraction(n1 + n2, d1),
        "resp_err_c-d": simplify_fraction(n1 * n2, d1 + d2),
        "resp_err_po-a": simplify_fraction(-correct_num, correct_den),
        "resp_err_po-b": simplify_fraction(1, correct_den),
        "resp_err_po-c": simplify_fraction(n1, d1 + d2) if op in ['+', '-'] else simplify_fraction(n1 * n2, d1 * d2 + 1),
        "resp_err_po-d": simplify_fraction(n1 * n2, d1 * d2 + 1),
        "resp_err_pf-a": simplify_fraction(n1 + n2, d1 + d2),
        "resp_err_pf-b": simplify_fraction(n1 + n2, d2),
        "resp_err_pf-c": simplify_fraction(n1 * d1, d2),
        "resp_err_pf-d": simplify_fraction(n1 + d1, n2 + d2),
        "resp_err_pf-e": simplify_fraction(n1, d1 * d2),
        "resp_err_s": f"{correct_num * 2}/{correct_den * 2}",
        "resp_err_a": simplify_fraction(correct_num + 1, correct_den),
    }
    
    user_answer = simplify_fraction(user_num, user_den)
    for error_code, incorrect_answer in errors.items():
        if user_answer == incorrect_answer:
            return error_code
    if user_answer == correct_answer:
        return "User has entered a Correct Answer"
    
    return "Unknown Error Type"

st.title("Mixed Fraction Error Checker")

whole1 = st.number_input("Whole Number 1", min_value=0, step=1)
numerator1 = st.number_input("Numerator 1", min_value=0, step=1)
denominator1 = st.number_input("Denominator 1", min_value=1, step=1)

operator = st.selectbox("Select Operator", ['+', '-', '×', '÷'])

whole2 = st.number_input("Whole Number 2", min_value=0, step=1)
numerator2 = st.number_input("Numerator 2", min_value=0, step=1)
denominator2 = st.number_input("Denominator 2", min_value=1, step=1)

wrong_answer = st.text_input("Enter the incorrect answer (in 'a/b' format)")

if st.button("Check Error"):
    try:
        f1 = convert_mixed_to_improper(whole1, numerator1, denominator1)
        f2 = convert_mixed_to_improper(whole2, numerator2, denominator2)
        
        wrong_fraction = tuple(map(int, wrong_answer.split('/')))
        
        correct = compute_correct_answer(f1, f2, operator)
        error_code = classify_error((*f1, operator, *f2, *wrong_fraction), correct)
        
        st.success(f"Correct Answer: {correct}")
        if(error_code == "User has entered a Correct Answer"):
            st.success("User has entered the correct answer")
        else:
            st.info(f"Identified Error Code: {error_code}")
    except Exception as e:
        st.error(f"Error: {e}")
