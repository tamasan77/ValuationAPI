from flask import Flask
from flask_restful import Api, Resource
import datetime
from datetime import timezone, timedelta
import math

app = Flask(__name__)
api = Api(app)

class Valuate():
    def price_forward(underlying_price, annual_risk_free_rate, valuation_date, expiration_date):
        """
        * @dev F(t) = S(t) * EXP(r(T-t))
        * F(t): forward price
        * t : valuation date
        * T : expiration date
        * T-t: seconds between valuation and expiration date
        * S(t): underlying asset price at valuation date
        * r(t): continuously compounded risk free interest rate on the valuation date
        """
        t_delta_years = (expiration_date - valuation_date)/ (365.25 * 86400)
        #risk_free_rate = ((annual_risk_free_rate / 365) / 86400)
        forward_price = underlying_price * math.e ** (annual_risk_free_rate * t_delta_years)
        return forward_price



class Pricing(Resource):
    def get(self, scaled_underlying_price, scaled_annual_risk_free_rate, valuation_date, expiration_date):
        #fixed-point numbers are scaled 1/100 for internal represenation within smart-contracts
        underlying_price = scaled_underlying_price / 100
        #divide by 10000 since it's percentage
        annual_risk_free_rate  =scaled_annual_risk_free_rate / 10000
        ffaPrice = Valuate.price_forward(underlying_price, annual_risk_free_rate, valuation_date, expiration_date)
        return {"price" : format(ffaPrice, '.2f')}


api.add_resource(Pricing, "/price/<int:scaled_underlying_price>/<int:scaled_annual_risk_free_rate>/<int:valuation_date>/<int:expiration_date>")

if __name__ == "__main__":
    app.run(debug=True)