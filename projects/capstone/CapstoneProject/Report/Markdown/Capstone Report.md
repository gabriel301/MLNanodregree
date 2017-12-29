
# Machine Learning Engineer Nanodegree
## Capstone Project: Building a Stock Price Predictor
Gabriel Augusto
December 29th, 2017

## I. Definition

### Project Overview
<p>The main objective for this project is to be capable to predict the <b>price of a given set stock</b> in a future time interval in days. In order to achieve the goal, Machine Learning techniques will be applied on the historical <b>adjusted close prices</b> for different stocks. </p>

#### What is a stock?

<p> According to Investopedia: <br>

"<i>A stock is a type of security that signifies ownership in a corporation and represents a claim on part of the corporation's assets and earnings. <br>
There are two main types of stock: common and preferred. Common stock usually entitles the owner to vote at shareholders' meetings and to receive dividends. Preferred stock generally does not have voting rights, but has a higher claim on assets and earnings than the common shares. For example, owners of preferred stock receive dividends before common shareholders and have priority in the event that a company goes bankrupt and is liquidated.</i>" [1] </p>

#### What is an exchange? <br>

<p>According to Investopedia: <br>

"<i>An exchange is a marketplace in which securities, commodities, derivatives and other financial instruments are traded. The core function of an exchange is to ensure fair and orderly trading, as well as efficient dissemination of price information for any securities trading on that exchange. Exchanges give companies, governments and other groups a platform to sell securities to the investing public. <br>
A stock exchange is used to raise capital for companies seeking to grow and expand their operations.</i>"[3]</p>

#### What is a company's worth, and who determines its stock price? <br>

<p> "<i> A company's worth, that is its total value,is its market capitalization, and it is represented by the company's stock price. Market cap (as it is commonly referred to) is equal to the stock price multiplied by the number of shares outstanding.</i> </p> 
<p> <i>For example, Microsoft (MSFT) is trading for 71.41 USD, as of August 10th 2017, and has 7.7 billion shares outstanding/trading. Therefore, the company is valued at 71.14 USD x 7.7 billion = 550 billion USD. Thus, the stock price is a relative and proportional value of a company's worth and only represents percentage changes in market cap at any given point in time. Any percentage changes in a stock price will result in an equal percentage change in a company's value. This is the reason why investors are so concerned with stock prices and any changes that may occur since a 0.10 USD drop in a stock can result in a 100,000 USD loss for shareholders with one million shares.</i> </p>
<p> <i>The next logical question is: Who sets stock prices and how are they calculated? In simple terms, the stock price of a company is calculated when a company goes public, an event called an initial public offering (IPO). This is when a company pays an investment bank lots of money to use very complex formulas and valuation techniques to derive a company's value and to determine how many shares will be offered to the public and at what price. </i></p>
<p> <i>After a company goes public and starts trading on the exchange, its price is determined by supply and demand for its shares in the market. If there is a high demand for its shares due to favorable factors, the price would increase. If the company's future growth potential doesn't look good, short sellers could drive down its price."</i> [4] </p>

#### What is an Adjusted Closing Price <br>
<p> "<i>An adjusted closing price is a stock's closing price on any given day of trading that has been amended to include any distributions and corporate actions such as __stock splits__, __dividends payments__ and __rights offerings__ that occurred at any time prior to the next day's open. The adjusted closing price is often used when examining historical returns or performing a detailed analysis on historical returns.</i> </p>

<p><i>A __stock split__ is a corporate action that is usually done by companies to make their share prices more marketable. A stock split does not affect a company's total market capitalization, but it does affect the company's stock price. Consequently, a company undergoing a stock split must adjust its closing price to depict the effect of the corporate action.</i>
</p>

<p><i>Common distributions that affect a stock's price include __cash dividends and stock dividends__. The difference between cash dividends and stock dividends is shareholders are entitled to a predetermined price per share and additional shares, respectively. For example, assume a company declared a 1 USD cash dividend and is trading at 51 USD per share on the ex-dividend date. On the ex-dividend date, the stock price is reduced by 1 USD and the adjusted closing price is 50 USD.</i>
</p>

<p><i>A stock's adjusted closing price also reflects __rights offerings__ that may occur. A rights offering is an issue of rights given to existing shareholders, which entitles the shareholders to subscribe to the rights issue in proportion to their shares. For example assume a company declares a rights offering, in which existing shareholders are entitled to one additional share for every two shares owned. Assume the stock is trading at 50 USD and existing shareholders are able to purchase additional shares at a subscription price of 45 USD. On the ex-date, the adjusted closing price is calculated based on the adjusting factor and the closing price.</i>"[5] </p>

#### The beginning <br>

<p>Back in the 15th century people already negotiated foreign currencies and valuable metals. At that time, some stock exchanges were created in Europe such as the "bourse" of Antwerp in Belgium (1561) and The Royal Exchange in England (1571).
The Dutch East India Company in Netherlands issued the first known stock certificate in 1606. This company traded spices between Amsterdam and East India (Indonesia) and operated similarly companies operate nowadays, with directors controlling company's operations and shareholders receiving a dividend of 16% per year. As the company issued shares on paper, investors also began to sell their shares to other investors. [2] </p>
<p>In the United States, the fisrt stock price was established in Philadelphia in 1790 and was called "The Board of Brokers". Now it is a part of NASDAQ, known as NASDAQ OMX PHLX. 
Shortly after the establisment of the Philadelphia Stock Exchange, the stock markert started to grow in New York, moved by 24 stock brokers outside of 68 Wall Street. As the market became more structured, in 1817 the New York Stock and Exchange Board was established.[2] </p>

### Problem Statement

<p>Given historical data for different stocks, is it possible to predict those stock prices for the future?
In order to implement this task, a data set with the <b>adjusted closed prices</b> is needed.<b>Adjusted closed prices</b> adjusts the close prices based on corporate actions (described in previous section) <br>
We will also calculate some <i>technical indicators</i> [7] for data, using them as input for the model. The following indicators are calculated: </p>
<p>
<b>Overlap Studies</b> <br>
<ul>
  <li>Bollinger Bands [7]</li>
  <li>Exponential Moving Average (EMA) [8]</li>
  <li>Simple Moving Average (SMA) [9]</li>
</ul>
</p>
<p>
<b>Momentum Indicators</b>
<ul>
  <li>Moving Average Convergence/Divergence (MACD) [10]</li>
  <li>Momentum [11]</li>
  <li>Relative Strength Index (RSI) [12]</li>
  <li>Stochastic Oscillator [21]</li>
</ul>
<br>
</p>

<p>For those tasks, TA-LIB library (http://mrjbq7.github.io/ta-lib/) will be used. <br> </p>
<p>
Thus the expected input for the <b>training algorithm</b> is: <br>
<ul>
  <li>A list of trade dates with its respectly high, low and adjusted closing prices</li>
  <li>A set of technical indicators calculated based on the input list described above.</li>
</ul>
</p>

<p>The expected input for the <b>Predictor</b> is: <br>
A list of stock symbols (aka companies tickers) and the number of days n ahead the price should be preditect.
<b>The expected output</b> is the price for each stock after n days. </p>

#### Problem Domain
<p>Since the problem consists in <b> to estimate the value </b> of future prices, which are <b>continuous quantitative data</b>, <b>a regressor is the right tool</b> to try to achieve this goal. </p>

<p>Althougth there are some challenges to tackle:
<ul>
  <li>Missing price values for different stocks and as well as in different dates</li>
  <li>Training cost, since there will be a fairly amount of historical data (almost 18 years)</li>
  <li>Response time: The algorithm should return an answer in a feasibile time</li>
  <li>Feature Engineering: Which features should be used?</li>
  <li>The estimative itself: Since the market is a very uncertain environment, how to fit a regressor in order to estimate stock prices?</li>
</ul> </p>

#### Task List
<p>In order to successfully estimate the prices, the following tasks are required:
<ul>
    <li>Download pricing data regarding the symbols queried</li>
    <li>Clean Data, which includes some strategy to fill missing values</li>
    <li>Calculate different technical indicators on data over the time</li>
    <li> Perform a model tuning in order to have the best model amongst different initial setups</li>
</ul></p>

### Metrics
<p>Since the proposed solution for this problem is a regression, the model metric chosen is the <b>coefficient of determination, also known as R2 Score</b>. <br>
The coefficient of determination is widely used to evaulate the goodness of fit of a model. It explains how well the predictions os a model approximates to the real data. <br>
R2 Score is scaled from 0 to 1, which 1 indicating a perfect fit of the model to data. </p>
<p> The <b>Mean Squared Error (MSE) </b> will also be computed, but only for comparision reasons. </p>

## II. Analysis
### Data Exploration and Exploratory Visualization
Data is downloaded from Yahoo Finance Website. In this analysis, we focus on stocks from B3 Exchange (former Bovespa) from Brazil. Data filename includes its provider, according with this source (https://help.yahoo.com/kb/SLN2310.html). For B3, the provider identifier is SA.
Historical data for the follow companies will be analyzed: <br>
- Embraer SA - EMBR3 (EMBR3.SA)
- Petrobras SA - PETR3 (PETR3.SA)
- Usiminas SA - USIM5 (USIM5.SA)

    Sample of file .\Data\Download\Historical\Yahoo\EMBR3.SA.csv

<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Date</th>
      <th>Ticker</th>
      <th>Open</th>
      <th>High</th>
      <th>Low</th>
      <th>Close</th>
      <th>Adjusted_Close</th>
      <th>Volume</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2000-01-03</td>
      <td>EMBR3</td>
      <td>7.75832</td>
      <td>7.75832</td>
      <td>7.00525</td>
      <td>7.16287</td>
      <td>6.364808</td>
      <td>1121444.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2000-01-04</td>
      <td>EMBR3</td>
      <td>6.83012</td>
      <td>6.83012</td>
      <td>6.30473</td>
      <td>6.30473</td>
      <td>5.602277</td>
      <td>1432068.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2000-01-05</td>
      <td>EMBR3</td>
      <td>6.45359</td>
      <td>6.59370</td>
      <td>6.21716</td>
      <td>6.54116</td>
      <td>5.812367</td>
      <td>1100888.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2000-01-06</td>
      <td>EMBR3</td>
      <td>6.47986</td>
      <td>6.47986</td>
      <td>6.30473</td>
      <td>6.33100</td>
      <td>5.625621</td>
      <td>523036.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2000-01-07</td>
      <td>EMBR3</td>
      <td>6.55867</td>
      <td>6.56743</td>
      <td>6.34851</td>
      <td>6.52364</td>
      <td>5.796801</td>
      <td>480782.0</td>
    </tr>
  </tbody>
</table>
</div>

<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Date</th>
      <th>Ticker</th>
      <th>Open</th>
      <th>High</th>
      <th>Low</th>
      <th>Close</th>
      <th>Adjusted_Close</th>
      <th>Volume</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4533</th>
      <td>2017-12-21</td>
      <td>EMBR3</td>
      <td>16.490000</td>
      <td>23.000000</td>
      <td>16.370001</td>
      <td>20.200001</td>
      <td>20.108690</td>
      <td>16687800.0</td>
    </tr>
    <tr>
      <th>4534</th>
      <td>2017-12-22</td>
      <td>EMBR3</td>
      <td>20.000000</td>
      <td>21.700001</td>
      <td>19.120001</td>
      <td>19.910000</td>
      <td>19.820000</td>
      <td>24817800.0</td>
    </tr>
    <tr>
      <th>4535</th>
      <td>2017-12-25</td>
      <td>EMBR3</td>
      <td>19.910000</td>
      <td>19.910000</td>
      <td>19.910000</td>
      <td>19.910000</td>
      <td>19.820000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4536</th>
      <td>2017-12-26</td>
      <td>EMBR3</td>
      <td>19.719999</td>
      <td>21.260000</td>
      <td>19.660000</td>
      <td>21.059999</td>
      <td>21.059999</td>
      <td>11824700.0</td>
    </tr>
    <tr>
      <th>4537</th>
      <td>2017-12-27</td>
      <td>EMBR3</td>
      <td>21.200001</td>
      <td>21.700001</td>
      <td>20.209999</td>
      <td>20.299999</td>
      <td>20.299999</td>
      <td>8180600.0</td>
    </tr>
  </tbody>
</table>
</div>

    Sample of file .\Data\Download\Historical\Yahoo\PETR3.SA.csv

<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Date</th>
      <th>Ticker</th>
      <th>Open</th>
      <th>High</th>
      <th>Low</th>
      <th>Close</th>
      <th>Adjusted_Close</th>
      <th>Volume</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2000-01-03</td>
      <td>PETR3</td>
      <td>3.06250</td>
      <td>3.06250</td>
      <td>3.06250</td>
      <td>3.06250</td>
      <td>2.809258</td>
      <td>3.998720e+09</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2000-01-04</td>
      <td>PETR3</td>
      <td>2.89063</td>
      <td>2.89063</td>
      <td>2.89063</td>
      <td>2.89063</td>
      <td>2.651600</td>
      <td>3.098880e+09</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2000-01-05</td>
      <td>PETR3</td>
      <td>2.92969</td>
      <td>2.92969</td>
      <td>2.92969</td>
      <td>2.92969</td>
      <td>2.687430</td>
      <td>6.645760e+09</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2000-01-06</td>
      <td>PETR3</td>
      <td>2.90625</td>
      <td>2.90625</td>
      <td>2.90625</td>
      <td>2.90625</td>
      <td>2.665929</td>
      <td>3.303680e+09</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2000-01-07</td>
      <td>PETR3</td>
      <td>2.92969</td>
      <td>2.92969</td>
      <td>2.92969</td>
      <td>2.92969</td>
      <td>2.687430</td>
      <td>2.506240e+09</td>
    </tr>
  </tbody>
</table>
</div>

<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Date</th>
      <th>Ticker</th>
      <th>Open</th>
      <th>High</th>
      <th>Low</th>
      <th>Close</th>
      <th>Adjusted_Close</th>
      <th>Volume</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4533</th>
      <td>2017-12-21</td>
      <td>PETR3</td>
      <td>16.000000</td>
      <td>16.650000</td>
      <td>15.990000</td>
      <td>16.650000</td>
      <td>16.650000</td>
      <td>5998700.0</td>
    </tr>
    <tr>
      <th>4534</th>
      <td>2017-12-22</td>
      <td>PETR3</td>
      <td>16.629999</td>
      <td>16.740000</td>
      <td>16.440001</td>
      <td>16.590000</td>
      <td>16.590000</td>
      <td>3666900.0</td>
    </tr>
    <tr>
      <th>4535</th>
      <td>2017-12-25</td>
      <td>PETR3</td>
      <td>16.590000</td>
      <td>16.590000</td>
      <td>16.590000</td>
      <td>16.590000</td>
      <td>16.590000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4536</th>
      <td>2017-12-26</td>
      <td>PETR3</td>
      <td>16.500000</td>
      <td>16.780001</td>
      <td>16.500000</td>
      <td>16.700001</td>
      <td>16.700001</td>
      <td>4180900.0</td>
    </tr>
    <tr>
      <th>4537</th>
      <td>2017-12-27</td>
      <td>PETR3</td>
      <td>16.799999</td>
      <td>16.980000</td>
      <td>16.730000</td>
      <td>16.760000</td>
      <td>16.760000</td>
      <td>4113900.0</td>
    </tr>
  </tbody>
</table>
</div>

    Sample of file .\Data\Download\Historical\Yahoo\USIM5.SA.csv
<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Date</th>
      <th>Ticker</th>
      <th>Open</th>
      <th>High</th>
      <th>Low</th>
      <th>Close</th>
      <th>Adjusted_Close</th>
      <th>Volume</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2000-01-03</td>
      <td>USIM5</td>
      <td>2.17778</td>
      <td>2.18000</td>
      <td>2.12222</td>
      <td>2.13333</td>
      <td>1.922614</td>
      <td>571500.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2000-01-04</td>
      <td>USIM5</td>
      <td>2.11111</td>
      <td>2.11111</td>
      <td>2.05556</td>
      <td>2.05556</td>
      <td>1.852526</td>
      <td>1121400.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2000-01-05</td>
      <td>USIM5</td>
      <td>2.06667</td>
      <td>2.25556</td>
      <td>2.05556</td>
      <td>2.25111</td>
      <td>2.028761</td>
      <td>1602450.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2000-01-06</td>
      <td>USIM5</td>
      <td>2.22222</td>
      <td>2.45556</td>
      <td>2.22222</td>
      <td>2.45556</td>
      <td>2.213016</td>
      <td>3084300.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2000-01-07</td>
      <td>USIM5</td>
      <td>2.45556</td>
      <td>2.57778</td>
      <td>2.44444</td>
      <td>2.55333</td>
      <td>2.301129</td>
      <td>2871000.0</td>
    </tr>
  </tbody>
</table>
</div>

<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Date</th>
      <th>Ticker</th>
      <th>Open</th>
      <th>High</th>
      <th>Low</th>
      <th>Close</th>
      <th>Adjusted_Close</th>
      <th>Volume</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4533</th>
      <td>2017-12-21</td>
      <td>USIM5</td>
      <td>9.01</td>
      <td>9.20</td>
      <td>8.92</td>
      <td>9.05</td>
      <td>9.05</td>
      <td>15418500.0</td>
    </tr>
    <tr>
      <th>4534</th>
      <td>2017-12-22</td>
      <td>USIM5</td>
      <td>9.04</td>
      <td>9.09</td>
      <td>8.90</td>
      <td>8.95</td>
      <td>8.95</td>
      <td>6906500.0</td>
    </tr>
    <tr>
      <th>4535</th>
      <td>2017-12-25</td>
      <td>USIM5</td>
      <td>8.95</td>
      <td>8.95</td>
      <td>8.95</td>
      <td>8.95</td>
      <td>8.95</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4536</th>
      <td>2017-12-26</td>
      <td>USIM5</td>
      <td>8.88</td>
      <td>9.06</td>
      <td>8.82</td>
      <td>8.99</td>
      <td>8.99</td>
      <td>6293200.0</td>
    </tr>
    <tr>
      <th>4537</th>
      <td>2017-12-27</td>
      <td>USIM5</td>
      <td>9.06</td>
      <td>9.15</td>
      <td>9.04</td>
      <td>9.10</td>
      <td>9.10</td>
      <td>5571400.0</td>
    </tr>
  </tbody>
</table>
</div>


    Basic Descriptive Statistics for Data
    




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Ticker</th>
      <th>Min Date</th>
      <th>Max Date</th>
      <th>Count</th>
      <th>Mean</th>
      <th>Std</th>
      <th>Min</th>
      <th>25%</th>
      <th>50%</th>
      <th>75%</th>
      <th>Max</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>EMBR3</td>
      <td>2000-01-03</td>
      <td>2017-12-27</td>
      <td>4508.0</td>
      <td>14.263077</td>
      <td>4.941146</td>
      <td>5.267701</td>
      <td>10.396428</td>
      <td>13.554510</td>
      <td>17.771664</td>
      <td>29.660055</td>
    </tr>
    <tr>
      <th>1</th>
      <td>PETR3</td>
      <td>2000-01-03</td>
      <td>2017-12-27</td>
      <td>4505.0</td>
      <td>17.817948</td>
      <td>10.820841</td>
      <td>2.393607</td>
      <td>9.040000</td>
      <td>15.893916</td>
      <td>23.597769</td>
      <td>69.811775</td>
    </tr>
    <tr>
      <th>2</th>
      <td>USIM5</td>
      <td>2000-01-03</td>
      <td>2017-12-27</td>
      <td>4411.0</td>
      <td>10.315084</td>
      <td>8.308640</td>
      <td>0.730994</td>
      <td>3.340772</td>
      <td>8.900000</td>
      <td>14.529757</td>
      <td>44.150383</td>
    </tr>
  </tbody>
</table>
</div>



<p>Despite the three stocks have the same date range, they do not have the same row count (EMBR3 has the higher number of records and USIM5 has the lower number of records). </p>
<p>Given the fact above, it is very likely that these quotes miss data about some days over the years.</p>
<p>Below, the plot of adjusted close prices: </p>

![png](.\img\output_6_2.png)

Let's try to find out whether there are missing values

    Missing value count for each stock
<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>EMBR3</th>
      <th>PETR3</th>
      <th>USIM5</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>180.0</td>
      <td>198.0</td>
      <td>762.0</td>
    </tr>
  </tbody>
</table>
</div>

![png](.\img\output_8_3.png)


Data shows that USIM5 has the highest number of missing values, which explains why it has lower counting value than EMBR3, for instance. <br>

### Algorithm and Techniques
As mentioned earlier, this is a <b> regression problem </b>. Hence, we are looking for models which approximate functions.
The following models may be considered (from simplest to the more complex):
<ol>
    <li><b>Generelized Linear Models</b> </li>
    <p> The simplest type of models, they are used when the result is expected to be a linear combination of the input. [13] </p>
    <li><b>Support Vector Machines with non-linear kernels</b> </li>
    <p> Support Vector Machines (SVM) and kernels provide us the ability of trying to fit data in a non-linear regression model.
        SVMs are very effective on High Dimensional Data and they are memory efficient as well. [14] </p>
</ol>
<br>
<p>Usually, the more complex the model is, the more is the likelihood of overfitting. Moreover, more complex models usually tends to take more time on training. Thus, the models used in this work will be chosen from the <b>Generelized Linear Models</b>. </p>
<p> The following models will be trained and tested</p>
<ul>
    <li>Ordinary Least Squares [15]</li>
    <li>Ridge Regression [16] </li>
    <li>Lasso [17] </li>
    <li>Elastic Net [18] </li>
    <li>Huber Regression [19] </li>
</ul>

<p>Before fitting the models, the input data will be preprocessed in order to handle missing values. Preprocessing also includes normalizing ajusted close prices and calculating the technical indicators described earlier. <br>
One more step is to tune the model in order to find the best parameters for each one. A Grid Search routine will perform this task as well as perform the model cross validation. </p>
<p> The final step is test the model predicting prices for 1, 7, 15, 30, 60 and 120 days ahead. </p>

### Benchmark
<p><b> Relative Error (also known as Approximation Error) </b> [20] will be used as benchmark for the predicted prices. <br> 
The goal is to achieve a error of +-5 % of the original price within 7 days.


## III. Methodology
### Data Preprocessing
<p>In order to make easier to have the code well organized, data pre-processing is made right after downloading. The function <b> DownloadData</b> from <b> StockHistoricalDataDownloader </b> module/class peforms the following tasks:</p>
<p>
<ol>
    <li>Download historical data from Yahoo Finance for the given stocks</li>
    <li>Fill Values Forward</li>
    <li>Fill Values Backward </li>
    <li>Sort rows by ascending date </li>
    <li>Normalize High, Low and Adjusted Closing Prices dividing all values by the first observation </li>
</ol>
</p>
<p>One might ask why does fill values forward and backwards instead filling with zeroes or interpoling. <br>
In this case, filling missing values with values with zeroes or interpoling might drastically change the result of calculation of technical indicators, as well as inserting new relationships that are not presenting in the original data.</p>
<p>Another question that might be arise is why does fill forward and then backward. The simple answer is that when missing values are found, we assume the last value known as valid. <br></p>
<p> Normalizing data is necessary because all data is re-scaled, and only the price variation is observed rather than the absolute values
</p>
<p> Below the comparision between original data and pre-processed data. For implemention details, please refer to <b>StockHistoricalDataDownloader</b> code.

    Sample of file .\Data\Quotes\Normalized\EMBR3.SA.csv
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Date</th>
      <th>Ticker</th>
      <th>Open</th>
      <th>High</th>
      <th>Low</th>
      <th>Close</th>
      <th>Adjusted_Close</th>
      <th>Volume</th>
      <th>Norm_High</th>
      <th>Norm_Low</th>
      <th>Norm_Adjusted_Close</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2000-01-03</td>
      <td>EMBR3</td>
      <td>7.75832</td>
      <td>7.75832</td>
      <td>7.00525</td>
      <td>7.16287</td>
      <td>6.364808</td>
      <td>1121444.0</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2000-01-04</td>
      <td>EMBR3</td>
      <td>6.83012</td>
      <td>6.83012</td>
      <td>6.30473</td>
      <td>6.30473</td>
      <td>5.602277</td>
      <td>1432068.0</td>
      <td>0.880361</td>
      <td>0.900001</td>
      <td>0.880196</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2000-01-05</td>
      <td>EMBR3</td>
      <td>6.45359</td>
      <td>6.59370</td>
      <td>6.21716</td>
      <td>6.54116</td>
      <td>5.812367</td>
      <td>1100888.0</td>
      <td>0.849888</td>
      <td>0.887500</td>
      <td>0.913204</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2000-01-06</td>
      <td>EMBR3</td>
      <td>6.47986</td>
      <td>6.47986</td>
      <td>6.30473</td>
      <td>6.33100</td>
      <td>5.625621</td>
      <td>523036.0</td>
      <td>0.835214</td>
      <td>0.900001</td>
      <td>0.883863</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2000-01-07</td>
      <td>EMBR3</td>
      <td>6.55867</td>
      <td>6.56743</td>
      <td>6.34851</td>
      <td>6.52364</td>
      <td>5.796801</td>
      <td>480782.0</td>
      <td>0.846502</td>
      <td>0.906250</td>
      <td>0.910758</td>
    </tr>
  </tbody>
</table>
</div>



<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Date</th>
      <th>Ticker</th>
      <th>Open</th>
      <th>High</th>
      <th>Low</th>
      <th>Close</th>
      <th>Adjusted_Close</th>
      <th>Volume</th>
      <th>Norm_High</th>
      <th>Norm_Low</th>
      <th>Norm_Adjusted_Close</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4533</th>
      <td>2017-12-21</td>
      <td>EMBR3</td>
      <td>16.490000</td>
      <td>23.000000</td>
      <td>16.370001</td>
      <td>20.200001</td>
      <td>20.108690</td>
      <td>16687800.0</td>
      <td>2.964559</td>
      <td>2.336819</td>
      <td>3.159355</td>
    </tr>
    <tr>
      <th>4534</th>
      <td>2017-12-22</td>
      <td>EMBR3</td>
      <td>20.000000</td>
      <td>21.700001</td>
      <td>19.120001</td>
      <td>19.910000</td>
      <td>19.820000</td>
      <td>24817800.0</td>
      <td>2.796997</td>
      <td>2.729382</td>
      <td>3.113998</td>
    </tr>
    <tr>
      <th>4535</th>
      <td>2017-12-25</td>
      <td>EMBR3</td>
      <td>19.910000</td>
      <td>19.910000</td>
      <td>19.910000</td>
      <td>19.910000</td>
      <td>19.820000</td>
      <td>0.0</td>
      <td>2.566277</td>
      <td>2.842154</td>
      <td>3.113998</td>
    </tr>
    <tr>
      <th>4536</th>
      <td>2017-12-26</td>
      <td>EMBR3</td>
      <td>19.719999</td>
      <td>21.260000</td>
      <td>19.660000</td>
      <td>21.059999</td>
      <td>21.059999</td>
      <td>11824700.0</td>
      <td>2.740284</td>
      <td>2.806467</td>
      <td>3.308819</td>
    </tr>
    <tr>
      <th>4537</th>
      <td>2017-12-27</td>
      <td>EMBR3</td>
      <td>21.200001</td>
      <td>21.700001</td>
      <td>20.209999</td>
      <td>20.299999</td>
      <td>20.299999</td>
      <td>8180600.0</td>
      <td>2.796997</td>
      <td>2.884979</td>
      <td>3.189413</td>
    </tr>
  </tbody>
</table>
</div>


    Sample of file .\Data\Quotes\Normalized\PETR3.SA.csv
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Date</th>
      <th>Ticker</th>
      <th>Open</th>
      <th>High</th>
      <th>Low</th>
      <th>Close</th>
      <th>Adjusted_Close</th>
      <th>Volume</th>
      <th>Norm_High</th>
      <th>Norm_Low</th>
      <th>Norm_Adjusted_Close</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2000-01-03</td>
      <td>PETR3</td>
      <td>3.06250</td>
      <td>3.06250</td>
      <td>3.06250</td>
      <td>3.06250</td>
      <td>2.809258</td>
      <td>3.998720e+09</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2000-01-04</td>
      <td>PETR3</td>
      <td>2.89063</td>
      <td>2.89063</td>
      <td>2.89063</td>
      <td>2.89063</td>
      <td>2.651600</td>
      <td>3.098880e+09</td>
      <td>0.943879</td>
      <td>0.943879</td>
      <td>0.943879</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2000-01-05</td>
      <td>PETR3</td>
      <td>2.92969</td>
      <td>2.92969</td>
      <td>2.92969</td>
      <td>2.92969</td>
      <td>2.687430</td>
      <td>6.645760e+09</td>
      <td>0.956633</td>
      <td>0.956633</td>
      <td>0.956633</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2000-01-06</td>
      <td>PETR3</td>
      <td>2.90625</td>
      <td>2.90625</td>
      <td>2.90625</td>
      <td>2.90625</td>
      <td>2.665929</td>
      <td>3.303680e+09</td>
      <td>0.948980</td>
      <td>0.948980</td>
      <td>0.948980</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2000-01-07</td>
      <td>PETR3</td>
      <td>2.92969</td>
      <td>2.92969</td>
      <td>2.92969</td>
      <td>2.92969</td>
      <td>2.687430</td>
      <td>2.506240e+09</td>
      <td>0.956633</td>
      <td>0.956633</td>
      <td>0.956633</td>
    </tr>
  </tbody>
</table>
</div>



<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Date</th>
      <th>Ticker</th>
      <th>Open</th>
      <th>High</th>
      <th>Low</th>
      <th>Close</th>
      <th>Adjusted_Close</th>
      <th>Volume</th>
      <th>Norm_High</th>
      <th>Norm_Low</th>
      <th>Norm_Adjusted_Close</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4533</th>
      <td>2017-12-21</td>
      <td>PETR3</td>
      <td>16.000000</td>
      <td>16.650000</td>
      <td>15.990000</td>
      <td>16.650000</td>
      <td>16.650000</td>
      <td>5998700.0</td>
      <td>5.436735</td>
      <td>5.221224</td>
      <td>5.926832</td>
    </tr>
    <tr>
      <th>4534</th>
      <td>2017-12-22</td>
      <td>PETR3</td>
      <td>16.629999</td>
      <td>16.740000</td>
      <td>16.440001</td>
      <td>16.590000</td>
      <td>16.590000</td>
      <td>3666900.0</td>
      <td>5.466122</td>
      <td>5.368164</td>
      <td>5.905474</td>
    </tr>
    <tr>
      <th>4535</th>
      <td>2017-12-25</td>
      <td>PETR3</td>
      <td>16.590000</td>
      <td>16.590000</td>
      <td>16.590000</td>
      <td>16.590000</td>
      <td>16.590000</td>
      <td>0.0</td>
      <td>5.417143</td>
      <td>5.417143</td>
      <td>5.905474</td>
    </tr>
    <tr>
      <th>4536</th>
      <td>2017-12-26</td>
      <td>PETR3</td>
      <td>16.500000</td>
      <td>16.780001</td>
      <td>16.500000</td>
      <td>16.700001</td>
      <td>16.700001</td>
      <td>4180900.0</td>
      <td>5.479184</td>
      <td>5.387755</td>
      <td>5.944631</td>
    </tr>
    <tr>
      <th>4537</th>
      <td>2017-12-27</td>
      <td>PETR3</td>
      <td>16.799999</td>
      <td>16.980000</td>
      <td>16.730000</td>
      <td>16.760000</td>
      <td>16.760000</td>
      <td>4113900.0</td>
      <td>5.544490</td>
      <td>5.462857</td>
      <td>5.965988</td>
    </tr>
  </tbody>
</table>
</div>


    Sample of file .\Data\Quotes\Normalized\USIM5.SA.csv
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Date</th>
      <th>Ticker</th>
      <th>Open</th>
      <th>High</th>
      <th>Low</th>
      <th>Close</th>
      <th>Adjusted_Close</th>
      <th>Volume</th>
      <th>Norm_High</th>
      <th>Norm_Low</th>
      <th>Norm_Adjusted_Close</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2000-01-03</td>
      <td>USIM5</td>
      <td>2.17778</td>
      <td>2.18000</td>
      <td>2.12222</td>
      <td>2.13333</td>
      <td>1.922614</td>
      <td>571500.0</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2000-01-04</td>
      <td>USIM5</td>
      <td>2.11111</td>
      <td>2.11111</td>
      <td>2.05556</td>
      <td>2.05556</td>
      <td>1.852526</td>
      <td>1121400.0</td>
      <td>0.968399</td>
      <td>0.968589</td>
      <td>0.963545</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2000-01-05</td>
      <td>USIM5</td>
      <td>2.06667</td>
      <td>2.25556</td>
      <td>2.05556</td>
      <td>2.25111</td>
      <td>2.028761</td>
      <td>1602450.0</td>
      <td>1.034661</td>
      <td>0.968589</td>
      <td>1.055210</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2000-01-06</td>
      <td>USIM5</td>
      <td>2.22222</td>
      <td>2.45556</td>
      <td>2.22222</td>
      <td>2.45556</td>
      <td>2.213016</td>
      <td>3084300.0</td>
      <td>1.126404</td>
      <td>1.047120</td>
      <td>1.151045</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2000-01-07</td>
      <td>USIM5</td>
      <td>2.45556</td>
      <td>2.57778</td>
      <td>2.44444</td>
      <td>2.55333</td>
      <td>2.301129</td>
      <td>2871000.0</td>
      <td>1.182468</td>
      <td>1.151832</td>
      <td>1.196875</td>
    </tr>
  </tbody>
</table>
</div>



<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Date</th>
      <th>Ticker</th>
      <th>Open</th>
      <th>High</th>
      <th>Low</th>
      <th>Close</th>
      <th>Adjusted_Close</th>
      <th>Volume</th>
      <th>Norm_High</th>
      <th>Norm_Low</th>
      <th>Norm_Adjusted_Close</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4533</th>
      <td>2017-12-21</td>
      <td>USIM5</td>
      <td>9.01</td>
      <td>9.20</td>
      <td>8.92</td>
      <td>9.05</td>
      <td>9.05</td>
      <td>15418500.0</td>
      <td>4.220183</td>
      <td>4.203146</td>
      <td>4.707133</td>
    </tr>
    <tr>
      <th>4534</th>
      <td>2017-12-22</td>
      <td>USIM5</td>
      <td>9.04</td>
      <td>9.09</td>
      <td>8.90</td>
      <td>8.95</td>
      <td>8.95</td>
      <td>6906500.0</td>
      <td>4.169725</td>
      <td>4.193722</td>
      <td>4.655121</td>
    </tr>
    <tr>
      <th>4535</th>
      <td>2017-12-25</td>
      <td>USIM5</td>
      <td>8.95</td>
      <td>8.95</td>
      <td>8.95</td>
      <td>8.95</td>
      <td>8.95</td>
      <td>0.0</td>
      <td>4.105505</td>
      <td>4.217282</td>
      <td>4.655121</td>
    </tr>
    <tr>
      <th>4536</th>
      <td>2017-12-26</td>
      <td>USIM5</td>
      <td>8.88</td>
      <td>9.06</td>
      <td>8.82</td>
      <td>8.99</td>
      <td>8.99</td>
      <td>6293200.0</td>
      <td>4.155963</td>
      <td>4.156025</td>
      <td>4.675926</td>
    </tr>
    <tr>
      <th>4537</th>
      <td>2017-12-27</td>
      <td>USIM5</td>
      <td>9.06</td>
      <td>9.15</td>
      <td>9.04</td>
      <td>9.10</td>
      <td>9.10</td>
      <td>5571400.0</td>
      <td>4.197248</td>
      <td>4.259690</td>
      <td>4.733139</td>
    </tr>
  </tbody>
</table>
</div>


    Basic Descriptive Statistics for Pre-Processed Data (Adjusted_Close Column)
    




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Ticker</th>
      <th>Min Date</th>
      <th>Max Date</th>
      <th>Count</th>
      <th>Mean</th>
      <th>Std</th>
      <th>Min</th>
      <th>25%</th>
      <th>50%</th>
      <th>75%</th>
      <th>Max</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>EMBR3</td>
      <td>2000-01-03</td>
      <td>2017-12-27</td>
      <td>4538.0</td>
      <td>14.281463</td>
      <td>4.955458</td>
      <td>5.267701</td>
      <td>10.415070</td>
      <td>13.554510</td>
      <td>17.777296</td>
      <td>29.660055</td>
    </tr>
    <tr>
      <th>1</th>
      <td>PETR3</td>
      <td>2000-01-03</td>
      <td>2017-12-27</td>
      <td>4538.0</td>
      <td>17.807229</td>
      <td>10.806457</td>
      <td>2.393607</td>
      <td>9.094619</td>
      <td>15.884347</td>
      <td>23.592885</td>
      <td>69.811775</td>
    </tr>
    <tr>
      <th>2</th>
      <td>USIM5</td>
      <td>2000-01-03</td>
      <td>2017-12-27</td>
      <td>4538.0</td>
      <td>10.221101</td>
      <td>8.274228</td>
      <td>0.730994</td>
      <td>3.168312</td>
      <td>8.791636</td>
      <td>14.451115</td>
      <td>44.150383</td>
    </tr>
  </tbody>
</table>
</div>



<p>In the pre-processed data, the new columns <b>Norm_High, Norm_Low and Norm_Adjusted_Close</b> is inserted. The first values are always 1 for all data because the first observations are the reference value. All other values represent the variation of the price between the current date and the first observed date. </p>
<p> Another difference is that now all stocks have no missing values. Stocks with data in the same date range now have the same counting number. <br>
Values for descriptive statistics also changed.</p>
<p>Below we verify the missing data counting: </p>

    Missing value count for each stock - Pre-processed dataset

<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>EMBR3</th>
      <th>PETR3</th>
      <th>USIM5</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>

The below figure shows the prices behaviour after pre-processing data:

![png](.\img\output_15_2.png)

![png](.\img\output_15_3.png)

<p> One might ask what the 'bar' in the plot for PETR3 stocks. It is a price peak in that specific day. Below, the information about the peak value:

    index                        2891
    Date                   2011-05-16
    Ticker                      PETR3
    Open                         73.6
    High                        75.55
    Low                          73.5
    Close                          74
    Adjusted_Close            69.8118
    Volume                      36511
    Norm_High                 24.6694
    Norm_Low                       24
    Norm_Adjusted_Close       24.8506

![png](.\img\output_17_2.png)

<p>After data cleaned, thechnical indicators are calculated for each ticker on Normalized High, Low and Price. Indicators parameters are informed in the code.</p>
<p>Below, the plots for a few indicators calculated: <p>

![png](.\img\output_19_1.png)

![png](.\img\output_19_2.png)

![png](.\img\output_19_3.png)

### Implementation
<p><b>Implementation Pipeline:</b><br>
<ol>
<li><b>Data Download</b></li>
Data is downloaded from Yahoo Finance website and salved as a csv file.
For doing that, it was necessary write a function that mimics a Web Browser in order to automatically download the data.
<li><b>Data Pre-processing</b></li>
After downloaded, all missing values are eliminated following the strategy forward-backward fill and prices are normalized by being divided by the first value observed.
<li><b>Featuring Engineering </b></li>
Techinal indicators below are calculated on the Normalized Adjusted Price using TA-Lib library. Results are append into the source dataset: <br>
<b>Overlap Studies</b> <br>
<ul>
  <li>Bollinger Bands [7]</li>
  <li>Exponential Moving Average (EMA) [8]</li>
  <li>Simple Moving Average (SMA) [9]</li>
</ul>  
<b>Momentum Indicators</b>
<ul>
  <li>Moving Average Convergence/Divergence (MACD) [10]</li>
  <li>Momentum [11]</li>
  <li>Relative Strength Index (RSI) [12]</li>
  <li>Stochastic Oscillator [21]</li>
</ul> 
</ol>
<li><b>Data splitting</b></li>
Data is splitted into training and testing datasets in ratio 80/20
<li><b> Cross Valitation </b></li>
Training data is shuffled and splitted again into training and testing datasets in ratio 80/20 by ShuffleSplit() Sklearn function
<li><b>Model Tuning </b> </li>
A Grid Search is performed for each model in order to find the best parameter combination
<li><b>Price Prediction </b> </li>
Prediction is performed with the testing dataset. Metrics and Benchmarks are computed for evaluation.
</p>

### Initial Results
<p> For the first implementation, the <b>Normalized High, Normalized Low, Normalized Adjusted Prices and the indicators</b> were considered as features. Below are the benchmarks for each model for predicting 1, 7, 15, 30, 60 and 120 days ahead:

<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.606253</td>
      <td>-0.595685</td>
      <td>0.150525</td>
      <td>0.656453</td>
      <td>-0.859632</td>
      <td>-36.277581</td>
      <td>-21.769928</td>
      <td>7.923385</td>
      <td>-28.050807</td>
      <td>-23.447941</td>
      <td>-16.034524</td>
      <td>12.016283</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.995464</td>
      <td>0.970200</td>
      <td>0.001734</td>
      <td>0.012259</td>
      <td>2.231627</td>
      <td>-9.387921</td>
      <td>-2.994812</td>
      <td>1.062398</td>
      <td>-3.614988</td>
      <td>-2.922919</td>
      <td>-2.322764</td>
      <td>1.292225</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.998550</td>
      <td>0.996275</td>
      <td>0.000554</td>
      <td>0.001532</td>
      <td>11.956129</td>
      <td>-14.864363</td>
      <td>-0.617636</td>
      <td>1.679888</td>
      <td>-1.534530</td>
      <td>-0.589090</td>
      <td>0.214982</td>
      <td>1.749512</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.998592</td>
      <td>0.996667</td>
      <td>0.000538</td>
      <td>0.001371</td>
      <td>13.033203</td>
      <td>-15.811529</td>
      <td>-0.526721</td>
      <td>1.786958</td>
      <td>-1.516526</td>
      <td>-0.523219</td>
      <td>0.390394</td>
      <td>1.906920</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.994947</td>
      <td>0.975305</td>
      <td>0.001932</td>
      <td>0.010159</td>
      <td>2.541191</td>
      <td>-9.157449</td>
      <td>-2.366555</td>
      <td>0.955355</td>
      <td>-2.915854</td>
      <td>-2.406783</td>
      <td>-1.874137</td>
      <td>1.041718</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 2 - Scores EMBR3 7 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.593052</td>
      <td>-0.488590</td>
      <td>0.155327</td>
      <td>0.612437</td>
      <td>-2.294828</td>
      <td>-32.955747</td>
      <td>-20.448803</td>
      <td>6.892421</td>
      <td>-25.876736</td>
      <td>-21.879951</td>
      <td>-15.265860</td>
      <td>10.610875</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.988600</td>
      <td>0.970187</td>
      <td>0.004351</td>
      <td>0.012266</td>
      <td>21.019137</td>
      <td>-18.974230</td>
      <td>-1.642213</td>
      <td>4.294554</td>
      <td>-4.473085</td>
      <td>-1.883270</td>
      <td>0.483923</td>
      <td>4.957009</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.996019</td>
      <td>0.993763</td>
      <td>0.001520</td>
      <td>0.002566</td>
      <td>30.743859</td>
      <td>-21.824577</td>
      <td>0.201776</td>
      <td>5.207437</td>
      <td>-2.976977</td>
      <td>0.033445</td>
      <td>2.664591</td>
      <td>5.641569</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.996091</td>
      <td>0.994009</td>
      <td>0.001492</td>
      <td>0.002465</td>
      <td>30.425646</td>
      <td>-22.310353</td>
      <td>0.101248</td>
      <td>5.265861</td>
      <td>-3.167058</td>
      <td>-0.104792</td>
      <td>2.585857</td>
      <td>5.752915</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.989303</td>
      <td>0.977834</td>
      <td>0.004083</td>
      <td>0.009120</td>
      <td>24.154492</td>
      <td>-19.220301</td>
      <td>-0.556520</td>
      <td>4.697608</td>
      <td>-3.569216</td>
      <td>-0.702046</td>
      <td>1.767827</td>
      <td>5.337043</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 3 - Scores EMBR3 15 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.576442</td>
      <td>-0.430693</td>
      <td>0.161405</td>
      <td>0.585989</td>
      <td>-3.487894</td>
      <td>-30.459152</td>
      <td>-19.500022</td>
      <td>6.115767</td>
      <td>-24.327867</td>
      <td>-21.041992</td>
      <td>-14.703725</td>
      <td>9.624142</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.989024</td>
      <td>0.978498</td>
      <td>0.004183</td>
      <td>0.008807</td>
      <td>37.885972</td>
      <td>-24.708964</td>
      <td>0.927940</td>
      <td>7.215961</td>
      <td>-4.065112</td>
      <td>0.469699</td>
      <td>4.441401</td>
      <td>8.506513</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.995810</td>
      <td>0.992955</td>
      <td>0.001597</td>
      <td>0.002886</td>
      <td>34.780125</td>
      <td>-26.304617</td>
      <td>0.294627</td>
      <td>7.632500</td>
      <td>-4.951681</td>
      <td>0.087525</td>
      <td>3.993608</td>
      <td>8.945289</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.995818</td>
      <td>0.993006</td>
      <td>0.001594</td>
      <td>0.002865</td>
      <td>34.776624</td>
      <td>-26.155788</td>
      <td>0.313598</td>
      <td>7.646369</td>
      <td>-4.954386</td>
      <td>0.109644</td>
      <td>4.044654</td>
      <td>8.999040</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.989058</td>
      <td>0.975467</td>
      <td>0.004170</td>
      <td>0.010048</td>
      <td>27.785877</td>
      <td>-23.868733</td>
      <td>-0.399429</td>
      <td>6.535186</td>
      <td>-5.026599</td>
      <td>-0.713448</td>
      <td>3.091334</td>
      <td>8.117933</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 4 - Scores EMBR3 30 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.512149</td>
      <td>-0.531545</td>
      <td>0.185195</td>
      <td>0.616316</td>
      <td>-3.696650</td>
      <td>-29.463888</td>
      <td>-19.356452</td>
      <td>5.697240</td>
      <td>-23.891765</td>
      <td>-20.815207</td>
      <td>-14.760365</td>
      <td>9.131401</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.954756</td>
      <td>0.898157</td>
      <td>0.017175</td>
      <td>0.040983</td>
      <td>51.267075</td>
      <td>-27.598500</td>
      <td>1.906223</td>
      <td>9.801541</td>
      <td>-5.081351</td>
      <td>0.386388</td>
      <td>6.577543</td>
      <td>11.658894</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.987583</td>
      <td>0.974473</td>
      <td>0.004713</td>
      <td>0.010272</td>
      <td>28.867267</td>
      <td>-26.575754</td>
      <td>1.283780</td>
      <td>10.307336</td>
      <td>-6.065112</td>
      <td>-0.377111</td>
      <td>6.759137</td>
      <td>12.824249</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.987589</td>
      <td>0.974522</td>
      <td>0.004712</td>
      <td>0.010253</td>
      <td>28.898934</td>
      <td>-26.745225</td>
      <td>1.267309</td>
      <td>10.318123</td>
      <td>-6.052673</td>
      <td>-0.365164</td>
      <td>6.794024</td>
      <td>12.846697</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.959124</td>
      <td>0.914781</td>
      <td>0.015517</td>
      <td>0.034293</td>
      <td>29.758685</td>
      <td>-29.231254</td>
      <td>-1.110882</td>
      <td>8.364312</td>
      <td>-7.241831</td>
      <td>-1.852620</td>
      <td>3.838007</td>
      <td>11.079838</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 5 - Scores EMBR3 60 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.363200</td>
      <td>-1.088886</td>
      <td>0.238840</td>
      <td>0.818740</td>
      <td>-2.800691</td>
      <td>-32.769992</td>
      <td>-21.351509</td>
      <td>6.368662</td>
      <td>-26.422112</td>
      <td>-22.895518</td>
      <td>-16.401027</td>
      <td>10.021085</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.824912</td>
      <td>0.710763</td>
      <td>0.065669</td>
      <td>0.113367</td>
      <td>57.714554</td>
      <td>-27.471708</td>
      <td>0.804681</td>
      <td>11.146128</td>
      <td>-6.920753</td>
      <td>-1.585713</td>
      <td>5.832483</td>
      <td>12.753236</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.954937</td>
      <td>0.900995</td>
      <td>0.016901</td>
      <td>0.038805</td>
      <td>46.025565</td>
      <td>-22.450769</td>
      <td>0.959988</td>
      <td>13.739042</td>
      <td>-8.988618</td>
      <td>-1.795165</td>
      <td>8.097179</td>
      <td>17.085796</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.954948</td>
      <td>0.900380</td>
      <td>0.016897</td>
      <td>0.039046</td>
      <td>46.347039</td>
      <td>-22.562503</td>
      <td>0.985725</td>
      <td>13.781169</td>
      <td>-9.018518</td>
      <td>-1.848468</td>
      <td>8.000821</td>
      <td>17.019339</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.831338</td>
      <td>0.653435</td>
      <td>0.063259</td>
      <td>0.135836</td>
      <td>28.784279</td>
      <td>-30.374319</td>
      <td>-3.831444</td>
      <td>8.447255</td>
      <td>-10.069206</td>
      <td>-4.936118</td>
      <td>1.472054</td>
      <td>11.541260</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 6 - Scores EMBR3 120 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.084458</td>
      <td>-3.588992</td>
      <td>0.338106</td>
      <td>1.749582</td>
      <td>0.869481</td>
      <td>-58.194001</td>
      <td>-33.208067</td>
      <td>13.745996</td>
      <td>-44.041624</td>
      <td>-35.697074</td>
      <td>-22.434308</td>
      <td>21.607317</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.583884</td>
      <td>-0.041173</td>
      <td>0.153670</td>
      <td>0.396954</td>
      <td>51.778006</td>
      <td>-28.361294</td>
      <td>-5.416418</td>
      <td>10.392714</td>
      <td>-12.270712</td>
      <td>-8.173388</td>
      <td>-1.077561</td>
      <td>11.193151</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.704066</td>
      <td>0.248243</td>
      <td>0.109287</td>
      <td>0.286612</td>
      <td>36.672752</td>
      <td>-31.206786</td>
      <td>-5.768576</td>
      <td>13.787296</td>
      <td>-16.119363</td>
      <td>-9.362364</td>
      <td>2.120708</td>
      <td>18.240071</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.704074</td>
      <td>0.248636</td>
      <td>0.109284</td>
      <td>0.286462</td>
      <td>36.959902</td>
      <td>-31.289444</td>
      <td>-5.763622</td>
      <td>13.828171</td>
      <td>-16.141576</td>
      <td>-9.337304</td>
      <td>1.972561</td>
      <td>18.114136</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.593072</td>
      <td>-0.158422</td>
      <td>0.150277</td>
      <td>0.441656</td>
      <td>22.431106</td>
      <td>-33.266043</td>
      <td>-9.439158</td>
      <td>8.370804</td>
      <td>-15.689044</td>
      <td>-10.701810</td>
      <td>-4.150519</td>
      <td>11.538525</td>
    </tr>
  </tbody>
</table>
</div>

![png](.\img\output_22_1.png)


![png](.\img\output_22_2.png)


![png](.\img\output_22_3.png)


![png](.\img\output_22_4.png)


![png](.\img\output_22_5.png)


![png](.\img\output_22_6.png)


![png](.\img\output_23_1.png)



![png](.\img\output_23_2.png)



![png](.\img\output_23_3.png)



![png](.\img\output_23_4.png)



![png](.\img\output_23_5.png)



![png](.\img\output_23_6.png)

<p>In general <b>Ordinary Least Squares (named Linear) and Rigde </b> were the <b>best models </b> when looking at R2 Score whereas <b>Elastic Net</b>  was the worse</p>
<p>The error variation was higher than the benchmark (+- 5%) for all models and all intervals except 1 day prediction for<b> EMBR3 </b> </p>
<p> Only <b>Elastic Net</b> model roughly exceed the benchmark interval for 1 day prediction. </p>

    Scores for 1 - Scores PETR3 1 days
    
<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.992178</td>
      <td>0.977446</td>
      <td>0.136200</td>
      <td>0.035272</td>
      <td>15.597986</td>
      <td>-6.853172</td>
      <td>2.213460</td>
      <td>3.169020</td>
      <td>0.246058</td>
      <td>2.224662</td>
      <td>4.133829</td>
      <td>3.887772</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.993044</td>
      <td>0.987853</td>
      <td>0.121110</td>
      <td>0.018997</td>
      <td>7.439043</td>
      <td>-9.167834</td>
      <td>-0.672902</td>
      <td>2.740574</td>
      <td>-2.451314</td>
      <td>-0.595942</td>
      <td>1.161230</td>
      <td>3.612544</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.997913</td>
      <td>0.994796</td>
      <td>0.036347</td>
      <td>0.008139</td>
      <td>11.794117</td>
      <td>-15.110638</td>
      <td>-0.191813</td>
      <td>3.442542</td>
      <td>-2.170889</td>
      <td>0.063680</td>
      <td>1.959371</td>
      <td>4.130260</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.997914</td>
      <td>0.994774</td>
      <td>0.036325</td>
      <td>0.008173</td>
      <td>11.763004</td>
      <td>-15.161734</td>
      <td>-0.197030</td>
      <td>3.440644</td>
      <td>-2.167797</td>
      <td>0.044619</td>
      <td>1.976613</td>
      <td>4.144410</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.993866</td>
      <td>0.985264</td>
      <td>0.106806</td>
      <td>0.023046</td>
      <td>10.821134</td>
      <td>-10.146188</td>
      <td>0.982435</td>
      <td>3.426900</td>
      <td>-1.307375</td>
      <td>1.000648</td>
      <td>3.132526</td>
      <td>4.439900</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 2 - Scores PETR3 7 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.990819</td>
      <td>0.948099</td>
      <td>0.160078</td>
      <td>0.081291</td>
      <td>28.432072</td>
      <td>-22.524165</td>
      <td>-2.454316</td>
      <td>6.877500</td>
      <td>-7.187385</td>
      <td>-3.457156</td>
      <td>1.059187</td>
      <td>8.246572</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.992764</td>
      <td>0.970664</td>
      <td>0.126155</td>
      <td>0.045948</td>
      <td>27.865278</td>
      <td>-33.313394</td>
      <td>-1.835439</td>
      <td>7.995749</td>
      <td>-6.860400</td>
      <td>-2.238216</td>
      <td>2.818359</td>
      <td>9.678758</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.995327</td>
      <td>0.990102</td>
      <td>0.081474</td>
      <td>0.015504</td>
      <td>35.920810</td>
      <td>-32.577144</td>
      <td>0.070965</td>
      <td>8.385365</td>
      <td>-5.427774</td>
      <td>-0.025732</td>
      <td>4.921793</td>
      <td>10.349567</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.995329</td>
      <td>0.990168</td>
      <td>0.081441</td>
      <td>0.015400</td>
      <td>36.092446</td>
      <td>-32.860212</td>
      <td>0.083817</td>
      <td>8.388766</td>
      <td>-5.421154</td>
      <td>0.018498</td>
      <td>4.924113</td>
      <td>10.345266</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.993415</td>
      <td>0.965295</td>
      <td>0.114814</td>
      <td>0.054357</td>
      <td>30.464276</td>
      <td>-32.631160</td>
      <td>-2.243691</td>
      <td>7.987164</td>
      <td>-7.672353</td>
      <td>-2.889936</td>
      <td>2.537556</td>
      <td>10.209909</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 3 - Scores PETR3 15 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.989125</td>
      <td>0.948467</td>
      <td>0.189898</td>
      <td>0.080744</td>
      <td>37.743080</td>
      <td>-25.977372</td>
      <td>1.136151</td>
      <td>8.405528</td>
      <td>-3.819798</td>
      <td>0.572830</td>
      <td>5.360962</td>
      <td>9.180761</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.992260</td>
      <td>0.974518</td>
      <td>0.135145</td>
      <td>0.039926</td>
      <td>52.399251</td>
      <td>-38.559379</td>
      <td>1.201518</td>
      <td>12.567274</td>
      <td>-6.064750</td>
      <td>0.163464</td>
      <td>8.166732</td>
      <td>14.231482</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.994823</td>
      <td>0.989246</td>
      <td>0.090400</td>
      <td>0.016850</td>
      <td>49.940284</td>
      <td>-35.763912</td>
      <td>0.928956</td>
      <td>12.954456</td>
      <td>-6.773492</td>
      <td>0.319380</td>
      <td>7.895894</td>
      <td>14.669386</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.994825</td>
      <td>0.989199</td>
      <td>0.090366</td>
      <td>0.016924</td>
      <td>50.048658</td>
      <td>-35.971280</td>
      <td>0.922564</td>
      <td>12.948205</td>
      <td>-6.761293</td>
      <td>0.308879</td>
      <td>7.825421</td>
      <td>14.586715</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.992482</td>
      <td>0.973150</td>
      <td>0.131285</td>
      <td>0.042069</td>
      <td>52.266337</td>
      <td>-36.404087</td>
      <td>1.981711</td>
      <td>12.143530</td>
      <td>-5.397458</td>
      <td>0.982202</td>
      <td>8.385076</td>
      <td>13.782534</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 4 - Scores PETR3 30 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.972478</td>
      <td>0.776066</td>
      <td>0.482029</td>
      <td>0.349738</td>
      <td>43.857872</td>
      <td>-23.184227</td>
      <td>5.524203</td>
      <td>9.854546</td>
      <td>-0.277244</td>
      <td>5.189942</td>
      <td>10.805989</td>
      <td>11.083233</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.988829</td>
      <td>0.949833</td>
      <td>0.195645</td>
      <td>0.078349</td>
      <td>75.775495</td>
      <td>-40.580011</td>
      <td>1.859414</td>
      <td>19.284926</td>
      <td>-11.163103</td>
      <td>-0.743956</td>
      <td>9.801368</td>
      <td>20.964471</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.990966</td>
      <td>0.958541</td>
      <td>0.158229</td>
      <td>0.064750</td>
      <td>74.009239</td>
      <td>-42.799932</td>
      <td>0.384534</td>
      <td>19.583950</td>
      <td>-12.296292</td>
      <td>-1.702111</td>
      <td>8.307423</td>
      <td>20.603715</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.990983</td>
      <td>0.958359</td>
      <td>0.157930</td>
      <td>0.065035</td>
      <td>73.737118</td>
      <td>-42.488506</td>
      <td>0.407556</td>
      <td>19.628323</td>
      <td>-12.246400</td>
      <td>-1.689649</td>
      <td>8.265037</td>
      <td>20.511437</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.989131</td>
      <td>0.950620</td>
      <td>0.190371</td>
      <td>0.077121</td>
      <td>73.150338</td>
      <td>-39.779099</td>
      <td>1.885642</td>
      <td>18.676874</td>
      <td>-9.902130</td>
      <td>-0.006054</td>
      <td>9.570119</td>
      <td>19.472250</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 5 - Scores PETR3 60 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.914285</td>
      <td>-0.112793</td>
      <td>1.508592</td>
      <td>1.697072</td>
      <td>45.201018</td>
      <td>-14.632765</td>
      <td>11.659324</td>
      <td>10.063078</td>
      <td>4.899508</td>
      <td>11.622207</td>
      <td>18.090256</td>
      <td>13.190747</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.968061</td>
      <td>0.828270</td>
      <td>0.562134</td>
      <td>0.261898</td>
      <td>101.232509</td>
      <td>-52.277808</td>
      <td>3.933866</td>
      <td>27.499195</td>
      <td>-15.322558</td>
      <td>0.344528</td>
      <td>14.244271</td>
      <td>29.566829</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.978903</td>
      <td>0.865401</td>
      <td>0.371302</td>
      <td>0.205272</td>
      <td>122.304668</td>
      <td>-46.603677</td>
      <td>6.386929</td>
      <td>29.261528</td>
      <td>-14.491971</td>
      <td>1.421524</td>
      <td>17.817077</td>
      <td>32.309048</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.978905</td>
      <td>0.865451</td>
      <td>0.371271</td>
      <td>0.205196</td>
      <td>122.252756</td>
      <td>-46.613054</td>
      <td>6.391865</td>
      <td>29.280031</td>
      <td>-14.501937</td>
      <td>1.427718</td>
      <td>17.737482</td>
      <td>32.239419</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.965057</td>
      <td>0.715079</td>
      <td>0.615005</td>
      <td>0.434521</td>
      <td>95.829682</td>
      <td>-44.173786</td>
      <td>6.021269</td>
      <td>24.416581</td>
      <td>-10.386276</td>
      <td>3.815805</td>
      <td>15.879314</td>
      <td>26.265589</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 6 - Scores PETR3 120 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.791248</td>
      <td>-2.100530</td>
      <td>3.714647</td>
      <td>4.753960</td>
      <td>73.258359</td>
      <td>-9.455819</td>
      <td>24.306911</td>
      <td>14.649421</td>
      <td>13.578452</td>
      <td>24.174531</td>
      <td>33.848170</td>
      <td>20.269718</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.869815</td>
      <td>-1.294485</td>
      <td>2.316595</td>
      <td>3.518074</td>
      <td>129.865190</td>
      <td>-28.330193</td>
      <td>26.939469</td>
      <td>27.038123</td>
      <td>7.542617</td>
      <td>22.616686</td>
      <td>38.492474</td>
      <td>30.949857</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.880691</td>
      <td>-1.100577</td>
      <td>2.123060</td>
      <td>3.220760</td>
      <td>153.971659</td>
      <td>-30.338860</td>
      <td>27.578166</td>
      <td>32.200871</td>
      <td>4.329681</td>
      <td>21.488960</td>
      <td>40.543582</td>
      <td>36.213901</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.881053</td>
      <td>-1.096575</td>
      <td>2.116615</td>
      <td>3.214622</td>
      <td>152.684010</td>
      <td>-29.408503</td>
      <td>27.458658</td>
      <td>32.087575</td>
      <td>4.069934</td>
      <td>21.430184</td>
      <td>40.627339</td>
      <td>36.557405</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.860794</td>
      <td>-1.188595</td>
      <td>2.477110</td>
      <td>3.355714</td>
      <td>117.016669</td>
      <td>-32.329015</td>
      <td>24.221484</td>
      <td>26.022575</td>
      <td>6.051766</td>
      <td>21.313991</td>
      <td>34.926740</td>
      <td>28.874974</td>
    </tr>
  </tbody>
</table>
</div>

![png](.\img\output_26_1.png)



![png](.\img\output_26_2.png)



![png](.\img\output_26_3.png)



![png](.\img\output_26_4.png)



![png](.\img\output_26_5.png)



![png](.\img\output_26_6.png)

![png](.\img\output_27_1.png)



![png](.\img\output_27_2.png)



![png](.\img\output_27_3.png)



![png](.\img\output_27_4.png)



![png](.\img\output_27_5.png)



![png](.\img\output_27_6.png)


<p>Again, <b>Ordinary Least Squares (named Linear) and Rigde </b> were the <b>best models </b> when looking at R2 Score whereas <b>Elastic Net</b>  was the worse</p>
<p> Differently from <b>EMBR3 </b>, for <b>PETR4 Elastic Net</b> performed relatively well (> 0.75 R2 Score) for the first 4 tests (1, 7, 15 and 30 days) <p> 
<p> Even tough the R2 scores were similar, the relative error for <b>Huber</b> were closer to the benchmark than Ordinary Least Squares when predicting 1 day ahead.

    Scores for 1 - Scores USIM5 1 days

<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.997098</td>
      <td>0.949434</td>
      <td>0.058879</td>
      <td>0.069402</td>
      <td>47.822231</td>
      <td>-82.374677</td>
      <td>3.656323</td>
      <td>7.795957</td>
      <td>0.722308</td>
      <td>3.053067</td>
      <td>6.221529</td>
      <td>5.499222</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.998654</td>
      <td>0.970596</td>
      <td>0.027309</td>
      <td>0.040357</td>
      <td>37.829548</td>
      <td>-66.241001</td>
      <td>1.538249</td>
      <td>5.715024</td>
      <td>-0.865760</td>
      <td>1.052717</td>
      <td>3.372748</td>
      <td>4.238509</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.999489</td>
      <td>0.995018</td>
      <td>0.010368</td>
      <td>0.006838</td>
      <td>19.807619</td>
      <td>-22.564824</td>
      <td>0.288664</td>
      <td>4.005137</td>
      <td>-1.606896</td>
      <td>0.250165</td>
      <td>2.523403</td>
      <td>4.130299</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.999490</td>
      <td>0.995012</td>
      <td>0.010354</td>
      <td>0.006846</td>
      <td>19.906027</td>
      <td>-23.022162</td>
      <td>0.281776</td>
      <td>4.014943</td>
      <td>-1.625998</td>
      <td>0.270208</td>
      <td>2.489704</td>
      <td>4.115702</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.998424</td>
      <td>0.969151</td>
      <td>0.031970</td>
      <td>0.042340</td>
      <td>37.566580</td>
      <td>-72.663293</td>
      <td>1.013130</td>
      <td>5.873607</td>
      <td>-1.442971</td>
      <td>0.546928</td>
      <td>2.809427</td>
      <td>4.252397</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 2 - Scores USIM5 7 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.994695</td>
      <td>0.983101</td>
      <td>0.107764</td>
      <td>0.023101</td>
      <td>39.183955</td>
      <td>-28.695555</td>
      <td>1.992152</td>
      <td>9.395533</td>
      <td>-4.242867</td>
      <td>1.552141</td>
      <td>6.829949</td>
      <td>11.072816</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.996577</td>
      <td>0.989152</td>
      <td>0.069521</td>
      <td>0.014830</td>
      <td>34.497817</td>
      <td>-46.946164</td>
      <td>0.093789</td>
      <td>10.916147</td>
      <td>-6.335657</td>
      <td>-0.079468</td>
      <td>6.189736</td>
      <td>12.525393</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.998684</td>
      <td>0.993469</td>
      <td>0.026740</td>
      <td>0.008928</td>
      <td>36.549622</td>
      <td>-53.935403</td>
      <td>0.618660</td>
      <td>11.688447</td>
      <td>-5.985660</td>
      <td>1.293642</td>
      <td>7.060535</td>
      <td>13.046195</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.998685</td>
      <td>0.993506</td>
      <td>0.026715</td>
      <td>0.008878</td>
      <td>36.723635</td>
      <td>-54.035171</td>
      <td>0.626696</td>
      <td>11.706868</td>
      <td>-5.866087</td>
      <td>1.291687</td>
      <td>7.092559</td>
      <td>12.958646</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.996683</td>
      <td>0.988051</td>
      <td>0.067371</td>
      <td>0.016334</td>
      <td>38.567316</td>
      <td>-48.440803</td>
      <td>0.341662</td>
      <td>11.497421</td>
      <td>-6.842667</td>
      <td>-0.065668</td>
      <td>6.869325</td>
      <td>13.711993</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 3 - Scores USIM5 15 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.993228</td>
      <td>0.959826</td>
      <td>0.137770</td>
      <td>0.054824</td>
      <td>59.027108</td>
      <td>-46.503349</td>
      <td>4.951329</td>
      <td>13.700595</td>
      <td>-4.106784</td>
      <td>4.285150</td>
      <td>11.819357</td>
      <td>15.926141</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.995989</td>
      <td>0.981007</td>
      <td>0.081603</td>
      <td>0.025919</td>
      <td>60.555872</td>
      <td>-64.734885</td>
      <td>0.570830</td>
      <td>17.799176</td>
      <td>-10.843921</td>
      <td>1.553187</td>
      <td>10.848411</td>
      <td>21.692332</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.998357</td>
      <td>0.995187</td>
      <td>0.033428</td>
      <td>0.006569</td>
      <td>63.904203</td>
      <td>-58.479136</td>
      <td>1.965894</td>
      <td>18.539928</td>
      <td>-8.888380</td>
      <td>2.043435</td>
      <td>12.179287</td>
      <td>21.067667</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.998361</td>
      <td>0.995177</td>
      <td>0.033345</td>
      <td>0.006581</td>
      <td>63.330688</td>
      <td>-58.536479</td>
      <td>1.967686</td>
      <td>18.504453</td>
      <td>-8.915409</td>
      <td>2.074933</td>
      <td>12.236464</td>
      <td>21.151872</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.995788</td>
      <td>0.980000</td>
      <td>0.085674</td>
      <td>0.027292</td>
      <td>66.031832</td>
      <td>-62.610050</td>
      <td>1.359259</td>
      <td>17.851000</td>
      <td>-9.951605</td>
      <td>1.615116</td>
      <td>11.553349</td>
      <td>21.504954</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 4 - Scores USIM5 30 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.971454</td>
      <td>0.823488</td>
      <td>0.582507</td>
      <td>0.241340</td>
      <td>72.035823</td>
      <td>-108.918187</td>
      <td>8.523486</td>
      <td>17.119252</td>
      <td>-1.554561</td>
      <td>7.580172</td>
      <td>16.880130</td>
      <td>18.434692</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.992029</td>
      <td>0.970982</td>
      <td>0.162645</td>
      <td>0.039675</td>
      <td>130.212911</td>
      <td>-41.487395</td>
      <td>6.616111</td>
      <td>29.079812</td>
      <td>-13.907742</td>
      <td>0.899667</td>
      <td>22.144904</td>
      <td>36.052645</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.994848</td>
      <td>0.982241</td>
      <td>0.105124</td>
      <td>0.024281</td>
      <td>134.582766</td>
      <td>-54.620649</td>
      <td>4.281055</td>
      <td>30.773208</td>
      <td>-17.145722</td>
      <td>1.291598</td>
      <td>22.168959</td>
      <td>39.314681</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.994849</td>
      <td>0.982241</td>
      <td>0.105102</td>
      <td>0.024281</td>
      <td>134.396420</td>
      <td>-54.660089</td>
      <td>4.282487</td>
      <td>30.760910</td>
      <td>-17.140415</td>
      <td>1.292541</td>
      <td>22.298751</td>
      <td>39.439165</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.993525</td>
      <td>0.974258</td>
      <td>0.132124</td>
      <td>0.035196</td>
      <td>127.389209</td>
      <td>-55.490430</td>
      <td>5.215996</td>
      <td>29.431690</td>
      <td>-14.931181</td>
      <td>2.702089</td>
      <td>21.785384</td>
      <td>36.716565</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 5 - Scores USIM5 60 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.882612</td>
      <td>0.586500</td>
      <td>2.410428</td>
      <td>0.561267</td>
      <td>67.909428</td>
      <td>-33.496976</td>
      <td>6.170869</td>
      <td>14.904938</td>
      <td>-3.783409</td>
      <td>4.409694</td>
      <td>13.186948</td>
      <td>16.970357</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.953994</td>
      <td>0.835753</td>
      <td>0.944690</td>
      <td>0.222941</td>
      <td>169.011941</td>
      <td>-52.188862</td>
      <td>8.670826</td>
      <td>36.690038</td>
      <td>-16.349991</td>
      <td>1.072909</td>
      <td>25.647955</td>
      <td>41.997946</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.982794</td>
      <td>0.944793</td>
      <td>0.353303</td>
      <td>0.074936</td>
      <td>245.201582</td>
      <td>-72.751482</td>
      <td>11.746190</td>
      <td>50.321232</td>
      <td>-18.783314</td>
      <td>1.371226</td>
      <td>32.393417</td>
      <td>51.176731</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.982813</td>
      <td>0.944836</td>
      <td>0.352923</td>
      <td>0.074877</td>
      <td>245.890875</td>
      <td>-72.598173</td>
      <td>11.786344</td>
      <td>50.410646</td>
      <td>-18.702904</td>
      <td>1.383314</td>
      <td>32.543779</td>
      <td>51.246683</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.961818</td>
      <td>0.862072</td>
      <td>0.784024</td>
      <td>0.187217</td>
      <td>211.998931</td>
      <td>-49.557370</td>
      <td>13.317754</td>
      <td>42.752568</td>
      <td>-15.234415</td>
      <td>3.288122</td>
      <td>30.882472</td>
      <td>46.116887</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 6 - Scores USIM5 120 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.683691</td>
      <td>0.227100</td>
      <td>6.580172</td>
      <td>1.679926</td>
      <td>122.022557</td>
      <td>-14.128143</td>
      <td>21.106515</td>
      <td>21.640767</td>
      <td>7.881508</td>
      <td>16.414174</td>
      <td>27.426565</td>
      <td>19.545056</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.770464</td>
      <td>0.422066</td>
      <td>4.775040</td>
      <td>1.256160</td>
      <td>204.883462</td>
      <td>-39.288420</td>
      <td>21.748768</td>
      <td>38.639714</td>
      <td>-2.708181</td>
      <td>14.878668</td>
      <td>36.004536</td>
      <td>38.712718</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.831493</td>
      <td>0.521255</td>
      <td>3.505439</td>
      <td>1.040569</td>
      <td>297.038969</td>
      <td>-51.863459</td>
      <td>35.615800</td>
      <td>59.174663</td>
      <td>0.638749</td>
      <td>20.364170</td>
      <td>56.471271</td>
      <td>55.832523</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.831547</td>
      <td>0.521276</td>
      <td>3.504320</td>
      <td>1.040525</td>
      <td>295.543694</td>
      <td>-52.081743</td>
      <td>35.648702</td>
      <td>59.283103</td>
      <td>0.516548</td>
      <td>20.320230</td>
      <td>56.626363</td>
      <td>56.109815</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.798239</td>
      <td>0.444216</td>
      <td>4.197225</td>
      <td>1.208017</td>
      <td>263.271993</td>
      <td>-44.387744</td>
      <td>35.065176</td>
      <td>50.473118</td>
      <td>5.193338</td>
      <td>24.212324</td>
      <td>48.791075</td>
      <td>43.597737</td>
    </tr>
  </tbody>
</table>
</div>



![png](.\img\output_30_1.png)



![png](.\img\output_30_2.png)



![png](.\img\output_30_3.png)



![png](.\img\output_30_4.png)



![png](.\img\output_30_5.png)



![png](.\img\output_30_6.png)


![png](.\img\output_31_1.png)



![png](.\img\output_31_2.png)



![png](.\img\output_31_3.png)



![png](.\img\output_31_4.png)



![png](.\img\output_31_5.png)



![png](.\img\output_31_6.png)


<p>For the last stock, <b> USIM5 </b> the behaviour is consistent with the previous stocks</p>

<p>Observing all plots we can note that the relative error percentage increases when the time to predict increases and the R2 score decreases in the same situation. The error behaves usually like a normal distribution and each pair (model, days to predict) has different best models for the most times.</p>

### Refinement
<p> In order to get better results, we removed <b>Norm_High, Norm_Low and Norm_Adjusted_Close</b> as input features, leaving only the indicators calculated. <br>Another change was that indicators now are scaled between 0 and 1 before training the model. <br>
The results are discussed in the next section </p>


## IV. Results
### Model Evaluation and Validation
<p>For the new input, below are the benchmark plots: </p>


    Scores for 1 - Scores EMBR3 1 days

<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.562390</td>
      <td>0.034008</td>
      <td>0.167294</td>
      <td>0.397402</td>
      <td>-19.363554</td>
      <td>-19.365456</td>
      <td>-19.364212</td>
      <td>2.905924e-04</td>
      <td>-19.364418</td>
      <td>-19.364221</td>
      <td>-19.363997</td>
      <td>4.215032e-04</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.998251</td>
      <td>0.996599</td>
      <td>0.000669</td>
      <td>0.001399</td>
      <td>14.410804</td>
      <td>-13.682749</td>
      <td>0.176396</td>
      <td>1.856554e+00</td>
      <td>-0.839648</td>
      <td>0.132010</td>
      <td>1.117892</td>
      <td>1.957540e+00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.998510</td>
      <td>0.997162</td>
      <td>0.000570</td>
      <td>0.001167</td>
      <td>13.621038</td>
      <td>-13.631294</td>
      <td>0.043624</td>
      <td>1.757378e+00</td>
      <td>-0.918727</td>
      <td>0.026762</td>
      <td>0.896976</td>
      <td>1.815704e+00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.998539</td>
      <td>0.997255</td>
      <td>0.000559</td>
      <td>0.001129</td>
      <td>13.975211</td>
      <td>-14.049587</td>
      <td>0.017319</td>
      <td>1.790303e+00</td>
      <td>-0.997637</td>
      <td>0.004513</td>
      <td>0.928561</td>
      <td>1.926197e+00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.994228</td>
      <td>0.988099</td>
      <td>0.002207</td>
      <td>0.004896</td>
      <td>-0.261779</td>
      <td>-0.261779</td>
      <td>-0.261779</td>
      <td>9.537039e-11</td>
      <td>-0.261779</td>
      <td>-0.261779</td>
      <td>-0.261779</td>
      <td>1.552199e-10</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 2 - Scores EMBR3 7 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.533360</td>
      <td>-0.036796</td>
      <td>0.178111</td>
      <td>0.426560</td>
      <td>-19.573466</td>
      <td>-19.573466</td>
      <td>-19.573466</td>
      <td>7.685362e-11</td>
      <td>-19.573466</td>
      <td>-19.573466</td>
      <td>-19.573466</td>
      <td>1.250768e-10</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.993419</td>
      <td>0.988125</td>
      <td>0.002512</td>
      <td>0.004886</td>
      <td>28.277125</td>
      <td>-21.448921</td>
      <td>-0.099895</td>
      <td>4.952892e+00</td>
      <td>-3.035926</td>
      <td>-0.366869</td>
      <td>2.314514</td>
      <td>5.350440e+00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.995808</td>
      <td>0.993100</td>
      <td>0.001600</td>
      <td>0.002839</td>
      <td>29.799308</td>
      <td>-21.291576</td>
      <td>0.164742</td>
      <td>5.121558e+00</td>
      <td>-2.946954</td>
      <td>-0.027978</td>
      <td>2.637826</td>
      <td>5.584780e+00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.996105</td>
      <td>0.993903</td>
      <td>0.001487</td>
      <td>0.002508</td>
      <td>31.933350</td>
      <td>-22.723816</td>
      <td>0.256384</td>
      <td>5.359564e+00</td>
      <td>-3.046665</td>
      <td>0.041628</td>
      <td>2.772390</td>
      <td>5.819055e+00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.970957</td>
      <td>0.930957</td>
      <td>0.011086</td>
      <td>0.028406</td>
      <td>1.770734</td>
      <td>-3.194504</td>
      <td>-1.318575</td>
      <td>9.181862e-01</td>
      <td>-2.034871</td>
      <td>-1.472657</td>
      <td>-0.700638</td>
      <td>1.334233e+00</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 3 - Scores EMBR3 15 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.495611</td>
      <td>-0.135109</td>
      <td>0.192207</td>
      <td>0.464923</td>
      <td>-19.842729</td>
      <td>-19.842729</td>
      <td>-19.842729</td>
      <td>7.666289e-11</td>
      <td>-19.842729</td>
      <td>-19.842729</td>
      <td>-19.842729</td>
      <td>1.249241e-10</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.993781</td>
      <td>0.988696</td>
      <td>0.002370</td>
      <td>0.004630</td>
      <td>39.666546</td>
      <td>-29.241625</td>
      <td>0.504918</td>
      <td>7.940190e+00</td>
      <td>-4.742003</td>
      <td>0.118305</td>
      <td>4.249167</td>
      <td>8.991170e+00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.995626</td>
      <td>0.992471</td>
      <td>0.001667</td>
      <td>0.003084</td>
      <td>34.751837</td>
      <td>-26.701986</td>
      <td>0.357495</td>
      <td>7.558475e+00</td>
      <td>-4.873005</td>
      <td>0.179375</td>
      <td>3.961305</td>
      <td>8.834310e+00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.995824</td>
      <td>0.992989</td>
      <td>0.001591</td>
      <td>0.002871</td>
      <td>34.059027</td>
      <td>-25.750383</td>
      <td>0.311393</td>
      <td>7.590183e+00</td>
      <td>-4.936907</td>
      <td>0.122354</td>
      <td>4.060923</td>
      <td>8.997830e+00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.968195</td>
      <td>0.907986</td>
      <td>0.012120</td>
      <td>0.037687</td>
      <td>8.683844</td>
      <td>-8.880039</td>
      <td>-1.350895</td>
      <td>2.922248e+00</td>
      <td>-3.413362</td>
      <td>-1.699436</td>
      <td>0.516388</td>
      <td>3.929750e+00</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 4 - Scores EMBR3 30 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.417889</td>
      <td>-0.315650</td>
      <td>0.220977</td>
      <td>0.529436</td>
      <td>-20.375587</td>
      <td>-20.375587</td>
      <td>-20.375587</td>
      <td>7.615726e-11</td>
      <td>-20.375587</td>
      <td>-20.375587</td>
      <td>-20.375587</td>
      <td>1.237268e-10</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.982414</td>
      <td>0.968373</td>
      <td>0.006676</td>
      <td>0.012727</td>
      <td>29.782064</td>
      <td>-28.624354</td>
      <td>1.068647</td>
      <td>1.040865e+01</td>
      <td>-6.373750</td>
      <td>-0.253664</td>
      <td>7.014329</td>
      <td>1.338808e+01</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.987452</td>
      <td>0.974187</td>
      <td>0.004764</td>
      <td>0.010387</td>
      <td>28.433788</td>
      <td>-26.036941</td>
      <td>1.221749</td>
      <td>1.024463e+01</td>
      <td>-6.184836</td>
      <td>-0.396552</td>
      <td>6.632732</td>
      <td>1.281757e+01</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.987589</td>
      <td>0.974580</td>
      <td>0.004711</td>
      <td>0.010229</td>
      <td>28.907227</td>
      <td>-26.792068</td>
      <td>1.226525</td>
      <td>1.031841e+01</td>
      <td>-6.114970</td>
      <td>-0.429596</td>
      <td>6.743783</td>
      <td>1.285875e+01</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.960441</td>
      <td>0.910140</td>
      <td>0.015017</td>
      <td>0.036161</td>
      <td>15.083592</td>
      <td>-12.947192</td>
      <td>-1.447566</td>
      <td>5.850950e+00</td>
      <td>-6.007099</td>
      <td>-2.348182</td>
      <td>2.250871</td>
      <td>8.257970e+00</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 5 - Scores EMBR3 60 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.282483</td>
      <td>-0.751254</td>
      <td>0.269114</td>
      <td>0.686405</td>
      <td>-21.394440</td>
      <td>-21.408859</td>
      <td>-21.399434</td>
      <td>0.002216</td>
      <td>-21.401016</td>
      <td>-21.399543</td>
      <td>-21.397779</td>
      <td>0.003237</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.938081</td>
      <td>0.896158</td>
      <td>0.023224</td>
      <td>0.040701</td>
      <td>42.155193</td>
      <td>-26.884791</td>
      <td>0.932349</td>
      <td>13.389981</td>
      <td>-8.733154</td>
      <td>-2.003527</td>
      <td>8.288147</td>
      <td>17.021301</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.953971</td>
      <td>0.899385</td>
      <td>0.017264</td>
      <td>0.039436</td>
      <td>41.523721</td>
      <td>-20.874836</td>
      <td>0.853215</td>
      <td>13.176119</td>
      <td>-8.882400</td>
      <td>-1.834918</td>
      <td>8.140353</td>
      <td>17.022752</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.955123</td>
      <td>0.898355</td>
      <td>0.016832</td>
      <td>0.039840</td>
      <td>45.294366</td>
      <td>-21.429898</td>
      <td>1.040125</td>
      <td>13.596078</td>
      <td>-8.842159</td>
      <td>-1.567094</td>
      <td>7.917096</td>
      <td>16.759254</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.878503</td>
      <td>0.730818</td>
      <td>0.045569</td>
      <td>0.105506</td>
      <td>17.649637</td>
      <td>-17.121772</td>
      <td>-3.412031</td>
      <td>8.165076</td>
      <td>-9.687184</td>
      <td>-5.154937</td>
      <td>1.326489</td>
      <td>11.013673</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 6 - Scores EMBR3 120 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.038844</td>
      <td>-1.668201</td>
      <td>0.354951</td>
      <td>1.017269</td>
      <td>-23.212600</td>
      <td>-23.510978</td>
      <td>-23.316348</td>
      <td>0.046006</td>
      <td>-23.348917</td>
      <td>-23.318562</td>
      <td>-23.281789</td>
      <td>0.067128</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.684261</td>
      <td>0.247545</td>
      <td>0.116601</td>
      <td>0.286878</td>
      <td>34.372771</td>
      <td>-28.201497</td>
      <td>-5.179900</td>
      <td>12.938221</td>
      <td>-15.180562</td>
      <td>-8.393011</td>
      <td>2.092826</td>
      <td>17.273388</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.703399</td>
      <td>0.286941</td>
      <td>0.109533</td>
      <td>0.271858</td>
      <td>31.866367</td>
      <td>-27.189860</td>
      <td>-4.822781</td>
      <td>13.029329</td>
      <td>-14.470920</td>
      <td>-8.285173</td>
      <td>2.608453</td>
      <td>17.079373</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.704533</td>
      <td>0.296419</td>
      <td>0.109115</td>
      <td>0.268245</td>
      <td>35.512292</td>
      <td>-28.235661</td>
      <td>-4.638537</td>
      <td>13.443083</td>
      <td>-14.504831</td>
      <td>-8.225814</td>
      <td>2.680836</td>
      <td>17.185666</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.628716</td>
      <td>-0.080450</td>
      <td>0.137114</td>
      <td>0.411928</td>
      <td>12.397061</td>
      <td>-23.088274</td>
      <td>-9.332502</td>
      <td>8.126754</td>
      <td>-15.494960</td>
      <td>-11.698033</td>
      <td>-3.232464</td>
      <td>12.262496</td>
    </tr>
  </tbody>
</table>
</div>


![png](.\img\output_35_1.png)



![png](.\img\output_35_2.png)



![png](.\img\output_35_3.png)



![png](.\img\output_35_4.png)



![png](.\img\output_35_5.png)



![png](.\img\output_35_6.png)


![png](.\img\output_36_1.png)



![png](.\img\output_36_2.png)



![png](.\img\output_36_3.png)



![png](.\img\output_36_4.png)



![png](.\img\output_36_5.png)



![png](.\img\output_36_6.png)

<p> For <b>EMBR3 </b>, <b> Lasso </b> is the best overall model considering the metric, R2 Score, and the Benchmark. </p>
<p>For 1 prediction, the most part of models successfully beat the benchmark, whereas for 7 only Lasso was within the benchmark interval. </p>
<p>For the rest of predictions, despite Lasso had the best performance it could not be better than the benchmark. </p>

    Scores for 1 - Scores PETR3 1 days
    
<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.988948</td>
      <td>0.980047</td>
      <td>0.192435</td>
      <td>0.031205</td>
      <td>-1.729069</td>
      <td>-1.729069</td>
      <td>-1.729069</td>
      <td>6.844463e-11</td>
      <td>-1.729069</td>
      <td>-1.729069</td>
      <td>-1.729069</td>
      <td>1.075366e-10</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.994880</td>
      <td>0.993214</td>
      <td>0.089149</td>
      <td>0.010613</td>
      <td>7.280256</td>
      <td>-6.867901</td>
      <td>0.405544</td>
      <td>2.315439e+00</td>
      <td>-1.071354</td>
      <td>0.270736</td>
      <td>1.930372</td>
      <td>3.001725e+00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.997831</td>
      <td>0.995577</td>
      <td>0.037773</td>
      <td>0.006917</td>
      <td>11.743228</td>
      <td>-14.252436</td>
      <td>0.100642</td>
      <td>3.253763e+00</td>
      <td>-1.784711</td>
      <td>0.290200</td>
      <td>2.091428</td>
      <td>3.876139e+00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.997907</td>
      <td>0.994940</td>
      <td>0.036435</td>
      <td>0.007913</td>
      <td>12.268429</td>
      <td>-14.600795</td>
      <td>-0.027268</td>
      <td>3.339722e+00</td>
      <td>-1.920652</td>
      <td>0.162132</td>
      <td>1.994284</td>
      <td>3.914936e+00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.990335</td>
      <td>0.985619</td>
      <td>0.168281</td>
      <td>0.022492</td>
      <td>1.221488</td>
      <td>-1.385381</td>
      <td>-0.195275</td>
      <td>3.174725e-01</td>
      <td>-0.372466</td>
      <td>-0.212622</td>
      <td>-0.028656</td>
      <td>3.438099e-01</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 2 - Scores PETR3 7 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.976144</td>
      <td>0.890112</td>
      <td>0.415933</td>
      <td>0.172114</td>
      <td>-1.949358</td>
      <td>-1.949358</td>
      <td>-1.949358</td>
      <td>6.832036e-11</td>
      <td>-1.949358</td>
      <td>-1.949358</td>
      <td>-1.949358</td>
      <td>1.073868e-10</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.993199</td>
      <td>0.975457</td>
      <td>0.118582</td>
      <td>0.038441</td>
      <td>30.353608</td>
      <td>-35.460181</td>
      <td>-1.507246</td>
      <td>7.942894e+00</td>
      <td>-6.870123</td>
      <td>-2.001122</td>
      <td>3.180329</td>
      <td>1.005045e+01</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.995186</td>
      <td>0.988250</td>
      <td>0.083937</td>
      <td>0.018404</td>
      <td>34.549117</td>
      <td>-32.992574</td>
      <td>-0.218461</td>
      <td>8.333839e+00</td>
      <td>-5.552930</td>
      <td>-0.296377</td>
      <td>4.805594</td>
      <td>1.035852e+01</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.995329</td>
      <td>0.990141</td>
      <td>0.081435</td>
      <td>0.015442</td>
      <td>36.253601</td>
      <td>-32.766421</td>
      <td>0.175488</td>
      <td>8.486641e+00</td>
      <td>-5.417833</td>
      <td>0.059804</td>
      <td>5.062155</td>
      <td>1.047999e+01</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.986423</td>
      <td>0.957123</td>
      <td>0.236722</td>
      <td>0.067158</td>
      <td>17.231794</td>
      <td>-15.658849</td>
      <td>-0.164160</td>
      <td>4.338993e+00</td>
      <td>-3.005782</td>
      <td>-0.279616</td>
      <td>2.616140</td>
      <td>5.621923e+00</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 3 - Scores PETR3 15 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.960428</td>
      <td>0.771786</td>
      <td>0.690991</td>
      <td>0.357570</td>
      <td>-2.218350</td>
      <td>-2.218350</td>
      <td>-2.218350</td>
      <td>6.817897e-11</td>
      <td>-2.218350</td>
      <td>-2.218350</td>
      <td>-2.218350</td>
      <td>1.072116e-10</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.992695</td>
      <td>0.979553</td>
      <td>0.127563</td>
      <td>0.032036</td>
      <td>47.342270</td>
      <td>-41.765375</td>
      <td>0.645387</td>
      <td>1.247422e+01</td>
      <td>-6.448989</td>
      <td>0.355212</td>
      <td>7.533625</td>
      <td>1.398261e+01</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.994702</td>
      <td>0.988369</td>
      <td>0.092517</td>
      <td>0.018223</td>
      <td>50.406665</td>
      <td>-36.758691</td>
      <td>1.115568</td>
      <td>1.271836e+01</td>
      <td>-6.412042</td>
      <td>0.574860</td>
      <td>8.028953</td>
      <td>1.444099e+01</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.994832</td>
      <td>0.989237</td>
      <td>0.090249</td>
      <td>0.016863</td>
      <td>49.997382</td>
      <td>-35.834950</td>
      <td>0.708460</td>
      <td>1.293349e+01</td>
      <td>-6.877497</td>
      <td>0.132391</td>
      <td>7.661697</td>
      <td>1.453919e+01</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.988157</td>
      <td>0.965266</td>
      <td>0.206794</td>
      <td>0.054421</td>
      <td>44.640804</td>
      <td>-28.176139</td>
      <td>1.530287</td>
      <td>1.143382e+01</td>
      <td>-5.325158</td>
      <td>0.412540</td>
      <td>7.782469</td>
      <td>1.310763e+01</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 4 - Scores PETR3 30 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.932775</td>
      <td>0.550182</td>
      <td>1.177403</td>
      <td>0.702520</td>
      <td>-2.695136</td>
      <td>-2.695136</td>
      <td>-2.695136</td>
      <td>6.789549e-11</td>
      <td>-2.695136</td>
      <td>-2.695136</td>
      <td>-2.695136</td>
      <td>1.066316e-10</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.989078</td>
      <td>0.938007</td>
      <td>0.191296</td>
      <td>0.096820</td>
      <td>76.276761</td>
      <td>-41.483893</td>
      <td>-0.109195</td>
      <td>1.966181e+01</td>
      <td>-13.367683</td>
      <td>-2.680885</td>
      <td>7.653561</td>
      <td>2.102124e+01</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.990849</td>
      <td>0.958610</td>
      <td>0.160275</td>
      <td>0.064643</td>
      <td>75.448364</td>
      <td>-41.604496</td>
      <td>0.893195</td>
      <td>1.965318e+01</td>
      <td>-12.261594</td>
      <td>-1.482594</td>
      <td>9.024331</td>
      <td>2.128592e+01</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.990956</td>
      <td>0.960748</td>
      <td>0.158391</td>
      <td>0.061304</td>
      <td>75.212811</td>
      <td>-41.781594</td>
      <td>1.152681</td>
      <td>1.972079e+01</td>
      <td>-11.734866</td>
      <td>-1.321941</td>
      <td>9.435375</td>
      <td>2.117024e+01</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.984612</td>
      <td>0.939602</td>
      <td>0.269509</td>
      <td>0.094329</td>
      <td>66.281332</td>
      <td>-35.015894</td>
      <td>2.458139</td>
      <td>1.831882e+01</td>
      <td>-9.798560</td>
      <td>0.395182</td>
      <td>10.828538</td>
      <td>2.062710e+01</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 5 - Scores PETR3 60 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.868235</td>
      <td>-0.117719</td>
      <td>2.319080</td>
      <td>1.704585</td>
      <td>-3.732282</td>
      <td>-3.732282</td>
      <td>-3.732282</td>
      <td>6.724214e-11</td>
      <td>-3.732282</td>
      <td>-3.732282</td>
      <td>-3.732282</td>
      <td>1.053975e-10</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.963662</td>
      <td>0.768134</td>
      <td>0.639562</td>
      <td>0.353610</td>
      <td>100.131035</td>
      <td>-54.771582</td>
      <td>1.818608</td>
      <td>2.678730e+01</td>
      <td>-15.112319</td>
      <td>-1.451252</td>
      <td>12.490629</td>
      <td>2.760295e+01</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.977940</td>
      <td>0.877055</td>
      <td>0.388267</td>
      <td>0.187498</td>
      <td>115.140323</td>
      <td>-48.055185</td>
      <td>3.781028</td>
      <td>2.861725e+01</td>
      <td>-16.520765</td>
      <td>-0.209003</td>
      <td>14.634743</td>
      <td>3.115551e+01</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.978513</td>
      <td>0.881347</td>
      <td>0.378170</td>
      <td>0.180952</td>
      <td>119.424211</td>
      <td>-51.094731</td>
      <td>4.248012</td>
      <td>2.927984e+01</td>
      <td>-16.336738</td>
      <td>0.101217</td>
      <td>16.226043</td>
      <td>3.256278e+01</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.954141</td>
      <td>0.673921</td>
      <td>0.807123</td>
      <td>0.497288</td>
      <td>70.475498</td>
      <td>-38.168007</td>
      <td>1.825710</td>
      <td>2.025743e+01</td>
      <td>-12.044900</td>
      <td>-0.959749</td>
      <td>10.116746</td>
      <td>2.216165e+01</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 6 - Scores PETR3 120 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.733920</td>
      <td>-0.899630</td>
      <td>4.734782</td>
      <td>2.912652</td>
      <td>-5.946073</td>
      <td>-5.946073</td>
      <td>-5.946073</td>
      <td>6.594627e-11</td>
      <td>-5.946073</td>
      <td>-5.946073</td>
      <td>-5.946073</td>
      <td>1.034888e-10</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.847438</td>
      <td>-0.663350</td>
      <td>2.714780</td>
      <td>2.550370</td>
      <td>99.089379</td>
      <td>-44.662575</td>
      <td>13.340311</td>
      <td>2.464991e+01</td>
      <td>-2.766824</td>
      <td>12.158081</td>
      <td>26.819341</td>
      <td>2.958616e+01</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.870428</td>
      <td>-0.570202</td>
      <td>2.305687</td>
      <td>2.407550</td>
      <td>130.073749</td>
      <td>-43.757304</td>
      <td>17.473773</td>
      <td>3.097507e+01</td>
      <td>-4.842180</td>
      <td>14.540808</td>
      <td>32.670336</td>
      <td>3.751252e+01</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.871415</td>
      <td>-0.578605</td>
      <td>2.288123</td>
      <td>2.420434</td>
      <td>135.406834</td>
      <td>-45.456997</td>
      <td>18.047689</td>
      <td>3.194518e+01</td>
      <td>-5.339687</td>
      <td>14.795240</td>
      <td>34.206969</td>
      <td>3.954666e+01</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.840321</td>
      <td>-0.584037</td>
      <td>2.841416</td>
      <td>2.428762</td>
      <td>82.958724</td>
      <td>-37.742298</td>
      <td>12.181778</td>
      <td>2.234695e+01</td>
      <td>-2.547909</td>
      <td>10.536391</td>
      <td>22.980697</td>
      <td>2.552861e+01</td>
    </tr>
  </tbody>
</table>
</div>


![png](.\img\output_39_1.png)



![png](.\img\output_39_2.png)



![png](.\img\output_39_3.png)



![png](.\img\output_39_4.png)



![png](.\img\output_39_5.png)



![png](.\img\output_39_6.png)


![png](.\img\output_40_1.png)



![png](.\img\output_40_2.png)



![png](.\img\output_40_3.png)



![png](.\img\output_40_4.png)



![png](.\img\output_40_5.png)



![png](.\img\output_40_6.png)


<p><b>Elastic Net </b> was the best overall method for <b>PETR3</b> considering the benchmark. All other models were worse despite the R2 score of them was higher.</p>
<p>Incredibly, <b> Elastic Net </b> was very consistent and beat the benchmark roughly for all tests performed.</p>

    Scores for 1 - Scores USIM5 1 days
<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.996930</td>
      <td>0.991805</td>
      <td>0.062272</td>
      <td>0.011248</td>
      <td>-1.786910</td>
      <td>-1.786910</td>
      <td>-1.786910</td>
      <td>1.292474e-10</td>
      <td>-1.786910</td>
      <td>-1.786910</td>
      <td>-1.786910</td>
      <td>1.602340e-10</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.999061</td>
      <td>0.980914</td>
      <td>0.019048</td>
      <td>0.026196</td>
      <td>55.707014</td>
      <td>-28.267606</td>
      <td>-2.503040</td>
      <td>4.846024e+00</td>
      <td>-4.559596</td>
      <td>-2.377509</td>
      <td>-0.314134</td>
      <td>4.245462e+00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.999282</td>
      <td>0.997420</td>
      <td>0.014575</td>
      <td>0.003541</td>
      <td>18.140085</td>
      <td>-13.767537</td>
      <td>0.729210</td>
      <td>3.375924e+00</td>
      <td>-0.985864</td>
      <td>0.593914</td>
      <td>2.384046</td>
      <td>3.369911e+00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.999463</td>
      <td>0.996479</td>
      <td>0.010898</td>
      <td>0.004833</td>
      <td>20.736384</td>
      <td>-19.322475</td>
      <td>0.213430</td>
      <td>3.721740e+00</td>
      <td>-1.642691</td>
      <td>0.202987</td>
      <td>2.149278</td>
      <td>3.791969e+00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.997796</td>
      <td>0.993540</td>
      <td>0.044719</td>
      <td>0.008866</td>
      <td>3.224904</td>
      <td>-0.205914</td>
      <td>0.332709</td>
      <td>5.220945e-01</td>
      <td>0.053497</td>
      <td>0.210270</td>
      <td>0.390008</td>
      <td>3.365116e-01</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 2 - Scores USIM5 7 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.983572</td>
      <td>0.951048</td>
      <td>0.333691</td>
      <td>0.066918</td>
      <td>-2.049085</td>
      <td>-2.049085</td>
      <td>-2.049085</td>
      <td>1.289618e-10</td>
      <td>-2.049085</td>
      <td>-2.049085</td>
      <td>-2.049085</td>
      <td>1.599698e-10</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.996929</td>
      <td>0.989822</td>
      <td>0.062374</td>
      <td>0.013914</td>
      <td>32.519163</td>
      <td>-48.558584</td>
      <td>-0.008764</td>
      <td>1.088767e+01</td>
      <td>-6.626475</td>
      <td>-0.253943</td>
      <td>6.593976</td>
      <td>1.322045e+01</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.998428</td>
      <td>0.993082</td>
      <td>0.031921</td>
      <td>0.009457</td>
      <td>36.479158</td>
      <td>-52.769891</td>
      <td>0.903302</td>
      <td>1.160954e+01</td>
      <td>-6.187205</td>
      <td>1.212818</td>
      <td>7.374404</td>
      <td>1.356161e+01</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.998679</td>
      <td>0.993604</td>
      <td>0.026842</td>
      <td>0.008743</td>
      <td>36.245997</td>
      <td>-53.495622</td>
      <td>0.583799</td>
      <td>1.163398e+01</td>
      <td>-6.283287</td>
      <td>0.945095</td>
      <td>7.030665</td>
      <td>1.331395e+01</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.988097</td>
      <td>0.975623</td>
      <td>0.241774</td>
      <td>0.033324</td>
      <td>62.182957</td>
      <td>-39.103937</td>
      <td>0.581751</td>
      <td>1.156329e+01</td>
      <td>-5.699145</td>
      <td>0.155059</td>
      <td>4.129054</td>
      <td>9.828200e+00</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 3 - Scores USIM5 15 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.965527</td>
      <td>0.891664</td>
      <td>0.701272</td>
      <td>0.147839</td>
      <td>-2.405551</td>
      <td>-2.405551</td>
      <td>-2.405551</td>
      <td>1.286240e-10</td>
      <td>-2.405551</td>
      <td>-2.405551</td>
      <td>-2.405551</td>
      <td>1.597198e-10</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.996831</td>
      <td>0.985708</td>
      <td>0.064464</td>
      <td>0.019503</td>
      <td>64.196173</td>
      <td>-60.005372</td>
      <td>3.620681</td>
      <td>1.790298e+01</td>
      <td>-7.832999</td>
      <td>4.006457</td>
      <td>12.900267</td>
      <td>2.073327e+01</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.998203</td>
      <td>0.994622</td>
      <td>0.036565</td>
      <td>0.007339</td>
      <td>62.656382</td>
      <td>-59.465428</td>
      <td>1.982713</td>
      <td>1.829571e+01</td>
      <td>-8.800861</td>
      <td>2.232750</td>
      <td>11.579969</td>
      <td>2.038083e+01</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.998355</td>
      <td>0.995145</td>
      <td>0.033457</td>
      <td>0.006625</td>
      <td>65.372679</td>
      <td>-59.081815</td>
      <td>2.056677</td>
      <td>1.881107e+01</td>
      <td>-8.889201</td>
      <td>2.037558</td>
      <td>12.267806</td>
      <td>2.115701e+01</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.995251</td>
      <td>0.986527</td>
      <td>0.096607</td>
      <td>0.018386</td>
      <td>99.036913</td>
      <td>-66.187607</td>
      <td>3.664727</td>
      <td>2.144886e+01</td>
      <td>-9.425573</td>
      <td>3.221649</td>
      <td>13.351911</td>
      <td>2.277748e+01</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 4 - Scores USIM5 30 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.920275</td>
      <td>0.770239</td>
      <td>1.626844</td>
      <td>0.314145</td>
      <td>-3.288019</td>
      <td>-3.288019</td>
      <td>-3.288019</td>
      <td>1.276242e-10</td>
      <td>-3.288019</td>
      <td>-3.288019</td>
      <td>-3.288019</td>
      <td>1.581126e-10</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.993217</td>
      <td>0.972764</td>
      <td>0.138423</td>
      <td>0.037238</td>
      <td>134.333652</td>
      <td>-52.766415</td>
      <td>6.321297</td>
      <td>3.068881e+01</td>
      <td>-14.592343</td>
      <td>2.887017</td>
      <td>21.661309</td>
      <td>3.625365e+01</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.994750</td>
      <td>0.983178</td>
      <td>0.107123</td>
      <td>0.023000</td>
      <td>129.698919</td>
      <td>-53.994811</td>
      <td>4.014057</td>
      <td>2.995422e+01</td>
      <td>-17.451207</td>
      <td>1.190470</td>
      <td>21.609721</td>
      <td>3.906093e+01</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.994827</td>
      <td>0.984084</td>
      <td>0.105556</td>
      <td>0.021761</td>
      <td>128.298338</td>
      <td>-54.527658</td>
      <td>4.002243</td>
      <td>2.976162e+01</td>
      <td>-17.094439</td>
      <td>1.328390</td>
      <td>21.641150</td>
      <td>3.873559e+01</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.989047</td>
      <td>0.903182</td>
      <td>0.223506</td>
      <td>0.132376</td>
      <td>171.581586</td>
      <td>-102.242947</td>
      <td>10.027502</td>
      <td>3.552151e+01</td>
      <td>-13.206389</td>
      <td>6.299249</td>
      <td>26.485888</td>
      <td>3.969228e+01</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 5 - Scores USIM5 60 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.819615</td>
      <td>0.442182</td>
      <td>3.704002</td>
      <td>0.757157</td>
      <td>-5.264592</td>
      <td>-5.264592</td>
      <td>-5.264592</td>
      <td>1.253253e-10</td>
      <td>-5.264592</td>
      <td>-5.264592</td>
      <td>-5.264592</td>
      <td>1.565912e-10</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.969246</td>
      <td>0.913061</td>
      <td>0.631495</td>
      <td>0.118007</td>
      <td>248.163856</td>
      <td>-67.539541</td>
      <td>10.802144</td>
      <td>5.033551e+01</td>
      <td>-21.618634</td>
      <td>1.775992</td>
      <td>30.595700</td>
      <td>5.221433e+01</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.980973</td>
      <td>0.935095</td>
      <td>0.390691</td>
      <td>0.088099</td>
      <td>247.156644</td>
      <td>-70.380917</td>
      <td>13.612076</td>
      <td>4.993422e+01</td>
      <td>-16.536397</td>
      <td>3.911207</td>
      <td>32.592797</td>
      <td>4.912919e+01</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.982649</td>
      <td>0.947332</td>
      <td>0.356275</td>
      <td>0.071489</td>
      <td>250.175233</td>
      <td>-76.530033</td>
      <td>11.260626</td>
      <td>5.135365e+01</td>
      <td>-19.232718</td>
      <td>0.594141</td>
      <td>32.073171</td>
      <td>5.130589e+01</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.945799</td>
      <td>0.789577</td>
      <td>1.112956</td>
      <td>0.285619</td>
      <td>246.734248</td>
      <td>-56.544677</td>
      <td>18.075932</td>
      <td>4.765201e+01</td>
      <td>-12.707737</td>
      <td>10.466341</td>
      <td>36.516808</td>
      <td>4.922454e+01</td>
    </tr>
  </tbody>
</table>
</div>


    Scores for 6 - Scores USIM5 120 days
    


<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>R2 Training Score</th>
      <th>R2 Test Score</th>
      <th>MSE Train Score</th>
      <th>MSE Test Score</th>
      <th>Max Relative Error Percentage</th>
      <th>Min Relative Error Percentage</th>
      <th>Mean Relative Error Percentage</th>
      <th>Std Relative Error Percentage</th>
      <th>Q1 Relative Error Percentage</th>
      <th>Q2 Relative Error Percentage</th>
      <th>Q3 Relative Error Percentage</th>
      <th>IQR Relative Error Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElasticNet</td>
      <td>0.619948</td>
      <td>0.150809</td>
      <td>7.906221</td>
      <td>1.845748</td>
      <td>14.487458</td>
      <td>-8.677767</td>
      <td>-4.513549</td>
      <td>4.358307</td>
      <td>-6.844538</td>
      <td>-5.659728</td>
      <td>-4.493751</td>
      <td>2.350786</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Huber</td>
      <td>0.789195</td>
      <td>0.534832</td>
      <td>4.385364</td>
      <td>1.011059</td>
      <td>261.709425</td>
      <td>-77.434724</td>
      <td>11.029975</td>
      <td>53.156754</td>
      <td>-22.034729</td>
      <td>3.818073</td>
      <td>32.631738</td>
      <td>54.666467</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ridge</td>
      <td>0.820932</td>
      <td>0.557069</td>
      <td>3.725158</td>
      <td>0.962726</td>
      <td>457.345105</td>
      <td>-57.289119</td>
      <td>40.226101</td>
      <td>81.059517</td>
      <td>-3.730120</td>
      <td>21.494572</td>
      <td>61.373067</td>
      <td>65.103187</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Linear</td>
      <td>0.823136</td>
      <td>0.572363</td>
      <td>3.679299</td>
      <td>0.929485</td>
      <td>452.574485</td>
      <td>-63.503185</td>
      <td>38.550085</td>
      <td>81.828493</td>
      <td>-5.694089</td>
      <td>19.248229</td>
      <td>60.738621</td>
      <td>66.432710</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lasso</td>
      <td>0.774095</td>
      <td>0.456675</td>
      <td>4.699501</td>
      <td>1.180937</td>
      <td>434.703425</td>
      <td>-48.537648</td>
      <td>40.280720</td>
      <td>75.813949</td>
      <td>-0.699995</td>
      <td>24.781328</td>
      <td>56.807501</td>
      <td>57.507496</td>
    </tr>
  </tbody>
</table>
</div>

![png](.\img\output_43_1.png)



![png](.\img\output_43_2.png)



![png](.\img\output_43_3.png)



![png](.\img\output_43_4.png)



![png](.\img\output_43_5.png)



![png](.\img\output_43_6.png)


![png](.\img\output_44_1.png)



![png](.\img\output_44_2.png)



![png](.\img\output_44_3.png)



![png](.\img\output_44_4.png)



![png](.\img\output_44_5.png)



![png](.\img\output_44_6.png)


<p> Again, <b>Elastic Net</b> was the best overall model considering the benchmark, despite of not being the highest R2 Score. <p>
<p>For <b> USIM5 </b>, <b> Elastic Net</b> was worse than the benchmark only for 120 days prediction</p>
<p> Considering the facts above, <b> Elastic Net </b> is the chosen model. We will also plot <b> Lasso </b> for <b>EMBR</b> for comparision. </p>

### Justification
<p>Overall, the chosen model is stronger than benchmark. <br>
However, <b>the final solution is not significant</b> to solve the problem, because:</p>
<ol>
<li>The model does not perform reasonably for all stocks analyzed</li>
<li> Stock prices are influenced not only by past prices but also by other external factors, like news, market trust etc. The current model cannot find correlations between the prices and those external factors.</li>
<li> For short-term trading, 5% error is high and might not be useful since prices usually does not increases more than that value at the most part of time. For long-term trading, the model usually has a higher error rate that makes it unreliable.</li>
</ol>

## V. Conclusion
### Free-Form Visualization



![png](.\img\output_46_1.png)



![png](.\img\output_46_2.png)



![png](.\img\output_46_3.png)



![png](.\img\output_46_4.png)



![png](.\img\output_46_5.png)



![png](.\img\output_46_6.png)




![png](.\img\output_47_1.png)



![png](.\img\output_47_2.png)



![png](.\img\output_47_3.png)



![png](.\img\output_47_4.png)



![png](.\img\output_47_5.png)



![png](.\img\output_47_6.png)


![png](.\img\output_48_1.png)



![png](.\img\output_48_2.png)



![png](.\img\output_48_3.png)



![png](.\img\output_48_4.png)



![png](.\img\output_48_5.png)



![png](.\img\output_48_6.png)


### Reflection
<p>In this project we tried to predict stocks prices in a interval of 1, 7, 15, 30, 60 and 120 days ahead.
In order to successfully achieve the goal, the task list above was followed:
<ul>
<li>Download stock historical data</li>
<li>Fill Missing values</li>
<li>Normalized Prices</li>
<li>Calculate some techinal indicators on the data</li>
<li>Normalize techinal indicators</li>
<li>Train different models with the normalized indicators, using a Grid Search and performing cross-validation</li>
<li>Pick the best estimator</li>
</ul>
</p>
<p>An interest aspect of the projet is that there is no a good model that fits well in different stocks data and also in different time intervals. Thus, different stocks might have different models and the same data might have different estimators for different predicting intervals. <b>Hence, the final solution should not be used to predict different stock prices </b> despite of the fact it partially met the expectations of the project, that was to have a error range in +- %5 </p>

<p>There were 3 challenges: <br>
<ul>
    <li><b>Find a reliable free data source</b></li>
    For stocks that are not traded in US exchanges, is really difficult to find reliable free data source. Although I have downloaded data from Yahoo Finance, that data is not reliable because for many stocks I analyzed, there was lots of missing volume values, even when the price values were not missing.
    <li><b>Download Data from Yahoo Finance programatically</b></li>
    Despite Yahoo Finance is a free data source, it is difficult to programatically download its spreadsheets. The server rejects all requests that does not look like a web browser request as well as it embeds a code in the download url, rejecting the requests that does not pass the right code. Thus, it was a big challange to implement a method that successfully does the job.
    <li><b>Integrate the whole system</b></li>
    In order to met the project requirements, all modules of the final software were integrated. However, as they were implemented separately, some changes were needed in order to make them all integrated. In some cases, the whole method was refactored in order to make the integration easier.
</ul>
</p>

### Improvements

<p>I think the major improvement would be have one model that predicts relatively well for all type of stocks in a given interval. Thus, different models might predicts prices for different intervals (eg short-term and long-term)<br>
It is very likely that kind of solution already exists and perform better than the model chosen in this project</p>
<p>I would consider using Neural Networks, especially Deep Learning to try to predict prices. Perhaps, an Ensemble solution combining Unsupervised Learning for analyzing patterns for ups and downs in prices, neural networks for Natural Language Processing and Sentimental Analisys and Regression for calculating Technical Indicators and estimating the price. </p>


### References
[1]: https://www.investopedia.com/terms/s/stock.asp (Accessed in 2017-11-26)<br>
[2]: http://www.stock-trading-warrior.com/Origins-of-the-Stock-Market.html (Accessed in 2017-11-22) <br>
[3]: https://www.investopedia.com/terms/e/exchange.asp (Accessed in 2017-11-26)<br>
[4]: https://www.investopedia.com/ask/answers/133.asp?ad=dirN&qo=investopediaSiteSearch&qsrc=0&o=40186 (Accessed in 2017-11-26)<br>
[5]: https://www.investopedia.com/terms/a/adjusted_closing_price.asp (Accessed in 2017-11-26) <br>
[6]: https://en.wikipedia.org/wiki/Coefficient_of_determination (Accessed in 2017-11-26) <br>
[7]: https://www.investopedia.com/terms/b/bollingerbands.asp (Accessed in 2017-12-26) <br>
[8]: https://www.investopedia.com/terms/e/ema.asp (Accessed in 2017-12-26) <br>
[9]: https://www.investopedia.com/terms/s/sma.asp (Accessed in 2017-12-26) <br>
[10]: https://www.investopedia.com/terms/m/macd.asp (Accessed in 2017-12-26) <br>
[11]: https://www.investopedia.com/terms/m/momentum.asp (Accessed in 2017-12-26) <br>
[12]: https://www.investopedia.com/terms/r/rsi.asp (Accessed in 2017-12-26) <br>
[13]: http://scikit-learn.org/stable/modules/linear_model.html (Accessed in 2017-12-27) <br>
[14]: http://scikit-learn.org/stable/modules/svm.html (Accessed in 2017-12-27) <br>
[15]: http://scikit-learn.org/stable/modules/linear_model.html#ordinary-least-squares (Accessed in 2017-12-27) <br>
[16]: http://scikit-learn.org/stable/modules/linear_model.html#ridge-regression (Accessed in 2017-12-27) <br>
[17]: http://scikit-learn.org/stable/modules/linear_model.html#lasso (Accessed in 2017-12-27) <br>
[18]: http://scikit-learn.org/stable/modules/linear_model.html#elastic-net (Accessed in 2017-12-27) <br>
[19]: http://scikit-learn.org/stable/modules/linear_model.html#huber-regression (Accessed in 2017-12-27) <br>
[20]: https://en.wikipedia.org/wiki/Approximation_error (Accessed in 2017-12-27)
[21]: https://www.investopedia.com/terms/s/stochasticoscillator.asp (Accessed in 2017-12-26) <br>


```python

```
