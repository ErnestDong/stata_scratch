"""
run the script
"""
from app import app
import sourceCode.probit as probit
import sourceCode.logit as logit
import sourceCode.linear_reg as linear_reg
import sourceCode.exp_reg_model as exp_reg
import sourceCode.log_lin_model as log_lin
import sourceCode.lin_log_model as lin_log
import sourceCode.Colinearity as au_reg
import sourceCode.Hausman as HausmanTest
import sourceCode.White as WhiteTest
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
