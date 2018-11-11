#include "alwaysearn.hpp"
#include <eosiolib/eosio.hpp>
#include <eosiolib/asset.hpp>

namespace langchain {

void alwaysearn::addbid(
        eosio::name   name,
        std::string   strname,
        std::string   website,
        eosio::asset  price)
{

    _bidder bidderstable( _self, _self.value);
    bidderstable.emplace( _self, [&]( auto& s ) { 
       s.id         = bidderstable.available_primary_key();
       s.name       = name;
       s.strname    = strname;
       s.website    = website;
       s.price      = price;
    }); 

    _minprice pricetable(_self, _self.value);
    auto itr = pricetable.begin();
    if (itr == pricetable.end() ){
        pricetable.emplace(_self, [&](auto& s){
            s.id = 1;
            s.price = price;
        });
    } else if (itr->price < price){
        pricetable.modify(itr, _self, [&](auto& s){
            s.price = price;
        });
    }
}

void alwaysearn::deleteall(){
    require_auth(_self);
    _bidder bidderstable(_self, _self.value);

    auto itr = bidderstable.begin();
    while (itr != bidderstable.end() ){
       bidderstable.erase( itr );
       itr = bidderstable.begin();
    }
}

}

EOSIO_DISPATCH( langchain::alwaysearn, (addbid)(deleteall) )
