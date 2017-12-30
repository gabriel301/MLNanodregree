
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

The below figure shows the prices behaviour after pre-processing data:

![png](.\img\output_15_2.png)

![png](.\img\output_15_3.png)

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