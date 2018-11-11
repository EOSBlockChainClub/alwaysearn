#include "alwaysearn.hpp"

namespace langchain {

void alwaysearn::addbid(
        eosio::name   name,
        std::string   strname,
        std::string   website,
        uint64_t      price)
{

    bidder bidderstable( _self, _self);
    bidderstable.emplace( _self, [&]( auto& s ) { 
       s.id         = bidderstable.available_primary_key();
       s.name       = name;
       s.strname    = strname;
       s.website    = website;
       s.price      = price;
    }); 
}

void alwaysearn::deleteall(){
    require_auth(_self);
    bidder bidderstable(_self, _self);

    auto itr = bidderstable.begin();
    while (itr != bidderstable.end() ){
       bidderstable.erase( itr );
       itr = bidderstable.begin();
    }
}

EOSIO_DISPATCH( langchain::alwaysearn, (addbid)(deleteall) )
