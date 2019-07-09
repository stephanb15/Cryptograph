#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 15:17:10 2019

@author: stephan
"""

import math

class crymath:
    def extndEuclid(a,b):
        rtupel=[a,b]
        stupel=[1,0]
        while not(rtupel[1]==0):
            q=rtupel[0]//rtupel[1]
            saveR=rtupel[1]
            rtupel[1]=rtupel[0]-q*rtupel[1]
            rtupel[0]=saveR
            
            saveS=stupel[1]
            stupel[1]=stupel[0]-stupel[1]*q
            stupel[0]=saveS
            #uncooment for tests
            #print(rtupel,stupel)
        
        return (rtupel[0],stupel[0])
    
    def findrepres(rep,mod,bmax,bmin):
        #finds a representant "rep" of an equivalence class in certain borders
        #mathematically: trys to find a  $$ rep \in (bmin,bmax) $$
        #where the parantheses "(" and ")" indicate $$ bmin,bmax \notin (bmin,bmax) $$
        #thus indicate an open intervall
        #This function might loop infinitly if non proper borders are given
        if bmin>bmax:
            bmax,bmin=bmin,bmax
        if rep >= bmax:
            while rep>=bmax:
                rep=rep-mod
        if rep <= bmin:
            while rep<=bmin:
                rep=rep+mod
        #print("bmin",bmin,"bmax",bmax,"rep",rep,"mod",mod)
        return(rep)
        #Maybe write an error message when oscillation occurs:
        #Thus print a message when rep became >=bmax and later <=bmin
        #so then we know there is no such element $$ rep \in (bmin,bmax) $$
            
    def fastexp(base,power):
        #A function to make fast product calculation a^n,
        #where a, n are integers in this implementation
        #this function unfortunately is quiet as fast as the pythons power **
        #so imporvison might be necessary if possible
        #print("power",power)
        if power<=0:
            #this schouldn't actually occure for the public key
            return base**power
        
        binpow_str=bin(power)
        #convert binary string to list of "0" and "1"s
        binpow_intarr=[]
        
        for i in range(2,len(binpow_str)):
            #print(binpow_str)
            binpow_intarr.append(int(binpow_str[i]))
        binpow_intarr=binpow_intarr[::-1]
        #iterativ fast expoential calculation
        result=1
        for i in range(len(binpow_intarr)):
            if binpow_intarr[i]==1:
                result*=base**(2**i)
        return result
