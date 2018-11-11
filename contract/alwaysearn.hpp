#pragma once

#include <eosiolib/asset.hpp>
#include <eosiolib/eosio.hpp>

#include <string>

namespace langchain {

   class [[eosio::contract("alwaysearn")]] alwaysearn : public eosio::contract {
      private:
         struct [[eosio::table]] bidders{
             uint64_t       id;
             uint64_t       name;
             std::string    strname;
             std::string    website;
             uint64_t       price;

             uint64_t primary_key()const { return id; }
         };

         struct [[eosio::table]] minprices{
             uint64_t       price;

             uint64_t primary_key()const { return price; }
         };

      public:
         alwaysearn( eosio::name receiver, eosio::name code, eosio::datastream<const char*> ds ): eosio::contract(receiver, code, ds){}

         [[eosio::action]]
         void addbid( eosio::name  name,
                      std::string  strname,
                      std::string  website,
                      uint64_t     price);

         [[eosio::action]]
         void deleteall();

         typedef eosio::multi_index< "bidder"_n, bidders > bidder;
         typedef eosio::multi_index< "minprice"_n, minprices > minprice;

   };
}
