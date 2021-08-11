// jedicoins ICO

// version of compiler
pragma solidity ^0.4.11;

contract jedicoin_ico {
  // Introducing the maximum number of Jedicoins available for sale
  uint public max_jedicoins = 1000000;

  // Introducing USD-JC conversion rate
  uint public usd_to_jedicoins = 1;

  // Introducing the total number of Jedicoins that have been bought by investors
  uint public outstanding_jedicoins = 0;

  // Mapping from investor address to its equity in
  // Jedicoins and USD
  mapping(address => uint) equity_jedicoins;
  mapping(address => uint) equity_usd;

  // Check if investor can by jedicoins (any available?)
  modifier can_buy_jedicoins(uint usd_invested) {
    require(usd_invested * usd_to_jedicoins + outstanding_jedicoins <= max_jedicoins);
    _;
  }

  modifier can_sell_jedicoins(address investor, uint jedicoins_sold) {
    require(jedicoins_sold <= equity_jedicoins[investor]);
    _;
  }

  // Get the equity in jedicoins of an investor
  function equity_in_jedicoins(address investor) external constant returns (uint) {
    return equity_jedicoins(investor);
  }

  // Get the equity in usd of an investor
  function equity_in_usd(address investor) external constant returns (uint) {
    return equity_usd(investor);
  }

  // Buy jedicoins
  function buy_jedicoins(address investor, uint usd_invested) external 
  can_buy_jedicoins(usd_invested) {
    uint jedicoins_bought = usd_invested * usd_to_jedicoins;
    equity_in_jedicoins[investor] += jedicoins_bought;
    equity_in_usd[investor] += usd_invested;
    outstanding_jedicoins += jedicoins_bought;
  }

  // Sell jedicoins
  function sell_jedicoins(address investor, uint jedicoins_sold) external
  can_sell_jedicoins(investor, jedicoins_sold) {
    equity_jedicoins[investor] -= jedicoins_sold;
    equity_usd[investor] += jedicoins_sold / usd_to_jedicoins);
    outstanding_jedicoins -= jedicoins_sold;
  }



}