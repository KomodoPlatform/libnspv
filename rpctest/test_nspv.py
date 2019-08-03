#!/usr/bin/env python3
# Copyright (c) 2019 SuperNET developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from test_framework.nspvlib import NspvRpcCalls as tf
import time
import pytest


def setup_module():
    global real_addr, addr_send, wif_real, coin, call, chain_params
    real_addr = "RUp3xudmdTtxvaRnt3oq78FJBjotXy55uu"
    addr_send = "RNvAWip4DuFrZf8WhqdTBEcAg1bWjd4rKr"
    wif_real = "UsJgUBrmcsthJEGbyBBfD77tZ1FuRMkB68jqkP8E3PEE88eXesEH"

    if not real_addr or not addr_send or not wif_real:
        raise Exception("Please fill test parameters: ", real_addr, addr_send, wif_real)

    url = "http://127.0.0.1:12986"
    userpass = "userpass"
    coin = "ILN"
    call = tf(url, userpass)
    chain_params = {"KMD": {
                            'tx_list_address': 'RGShWG446Pv24CKzzxjA23obrzYwNbs1kA',
                            'min_chain_height': 1468080,
                            'notarization_height': '1468000',
                            'prev_notarization_h': 1467980,
                            'next_notarization_h': 1468020,
                            'hdrs_proof_low': '1468100',
                            'hdrs_proof_high': '1468200',
                            'numhdrs_expected': 151,
                            'tx_proof_id': 'f7beb36a65bc5bcbc9c8f398345aab7948160493955eb4a1f05da08c4ac3784f',
                            'tx_spent_height': 1456212,
                            'tx_proof_height': '1468520',
                           },
                    "ILN": {
                            'tx_list_address': 'RUp3xudmdTtxvaRnt3oq78FJBjotXy55uu',
                            'min_chain_height': 3689,
                            'notarization_height': '2000',
                            'prev_notarization_h': 1998,
                            'next_notarization_h': 2008,
                            'hdrs_proof_low': '2000',
                            'hdrs_proof_high': '2100',
                            'numhdrs_expected': 113,
                            'tx_proof_id': '67ffe0eaecd6081de04675c492a59090b573ee78955c4e8a85b8ac0be0e8e418',
                            'tx_spent_height': 2681,
                            'tx_proof_height': '2690',
                           }
                    }
    call.nspv_logout()


def test_help_call():
    """ Response should contain "result": "success"
        Response should contain actual help data"""
    print("testing help call")
    rpc_call = call.nspv_help()
    call.assert_success(rpc_call)
    call.assert_contains(rpc_call, "methods")


def test_getinfo_call():
    """ Response should contain "result": "success"
        Response should contain actual data"""
    print("testing getinfo call")
    rpc_call = call.nspv_getinfo()
    call.assert_success(rpc_call)
    call.assert_contains(rpc_call, "notarization")
    call.assert_contains(rpc_call, "header")

# call.assert_contains(rpc_call, "protocolversion")


# getpeerinfo call     -- needs it's own assertion and expected results WIP
# rpc_call = call.nspv_getpeerinfo(url, userpass)
# call.assert_success(rpc_call)


def test_hdrsproof_call():
    """ Response should be successful for case 2 and fail for others
        Response should contain actual headers"""
    print("testing hdrsproof call")
    prevheight = [False, chain_params.get(coin).get("hdrs_proof_low")]
    nextheight = [False, chain_params.get(coin).get("hdrs_proof_high")]
    # Case 1 - False data
    rpc_call = call.nspv_hdrsproof(prevheight[0], nextheight[0])
    call.assert_error(rpc_call)
    # Case 2 - known data
    rpc_call = call.nspv_hdrsproof(prevheight[1], nextheight[1])
    call.assert_success(rpc_call)
    call.assert_contains(rpc_call, "prevht")
    call.assert_contains(rpc_call, "nextht")
    call.assert_contains(rpc_call, "headers")
    rep = call.type_convert(rpc_call)
    hdrs_resp = rep.get('numhdrs')
    call.assert_equal(hdrs_resp, chain_params.get(coin).get("numhdrs_expected"))


def test_notarization_call():
    """ Response should be successful for case 2
     Successful response should contain prev and next notarizations data"""
    print("testing notarization call")
    height = [False, chain_params.get(coin).get("notarization_height")]
    # Case 1 - False data
    rpc_call = call.nspv_notarizations(height[0])
    call.assert_error(rpc_call)
    # Case 2 - known data
    rpc_call = call.nspv_notarizations(height[1])
    call.assert_success(rpc_call)
    call.assert_contains(rpc_call, "prev")
    call.assert_contains(rpc_call, "next")


def test_mempool_call():
    """ Response should contain txids"""
    print("testing mempool call")
    rpc_call = call.nspv_mempool()
    call.assert_success(rpc_call)
    call.assert_contains(rpc_call, "txids")

# TODO: set long autologout call


def test_logout_call():
    """ Runs here as fixture in case someone was already logged in"""
    rpc_call = call.nspv_logout()
    call.assert_success(rpc_call)


def getnewaddress_call():
    """ Get a new address, save it for latter calls"""
    print("testing getnewaddr call")
    rpc_call = call.nspv_getnewaddress()
    call.assert_contains(rpc_call, "wifprefix")
    call.assert_contains(rpc_call, "wif")
    call.assert_contains(rpc_call, "address")
    call.assert_contains(rpc_call, "pubkey")


def test_login_call():
    """"login with fresh credentials
        Response should contain address, address should be equal to generated earlier one"""
    print("testing log in call")
    rpc_call = call.nspv_getnewaddress()
    rep = call.type_convert(rpc_call)
    wif = rep.get('wif')
    addr = rep.get('address')
    rpc_call = call.nspv_login(wif)
    call.assert_success(rpc_call)
    call.assert_contains(rpc_call, "status")
    call.assert_contains(rpc_call, "address")
    rep = call.type_convert(rpc_call)
    address = rep.get('address')
    if address != addr:
        raise AssertionError("addr missmatch: ", addr, address)


def test_listtransactions_call():
    """"Successful response should [not] contain txids and same address ass requested
        Case 1 - False data, user is logged in - should not print txids for new address"""
    print("testing listtransactions call")
    rpc_call = call.nspv_getnewaddress()
    rep = call.type_convert(rpc_call)
    addr = rep.get('address')

    # Case 1 - False Data
    rpc_call = call.nspv_listtransactions(False, False, False)
    call.assert_success(rpc_call)
    call.assert_not_contains(rpc_call, "txids")
    rep = call.type_convert(rpc_call)
    addr_response = rep.get('address')
    if addr_response != addr:
        raise AssertionError("addr missmatch: ", addr_response, addr)

    # Case 2 - known data
    rpc_call = call.nspv_listtransactions(real_addr, 0, 1)
    call.assert_success(rpc_call)
    call.assert_contains(rpc_call, "txids")
    rep = call.type_convert(rpc_call)
    addr_response = rep.get('address')
    if addr_response != real_addr:
        raise AssertionError("addr missmatch: ", addr_response, real_addr)

    # Case 3 - known data, isCC = 1 is not valid for KMD chain, should not include txids
    rpc_call = call.nspv_listtransactions(real_addr, 1, 1)
    call.assert_success(rpc_call)
    call.assert_not_contains(rpc_call, "txids")
    rep = call.type_convert(rpc_call)
    addr_response = rep.get('address')
    if addr_response != real_addr:
        raise AssertionError("addr missmatch: ", addr_response, real_addr)

    # Case 4 - fresh generated data, should be no transactions yet
    rpc_call = call.nspv_listtransactions(addr, 0, 0)
    call.assert_success(rpc_call)
    call.assert_not_contains(rpc_call, "txids")
    rep = call.type_convert(rpc_call)
    addr_response = rep.get('address')
    if addr_response != addr:
        raise AssertionError("addr missmatch: ", addr_response, addr)


def test_litunspent_call():
    """ Successful response should [not] contain utxos and same address as requested"""
    print("testing listunspent call")
    rpc_call = call.nspv_getnewaddress()
    rep = call.type_convert(rpc_call)
    addr = rep.get('address')

    # Case 1 - False data, user is logged in - should pas, print no utxos for fresh address
    rpc_call = call.nspv_listunspent(False, False, False)
    call.assert_success(rpc_call)
    call.assert_not_contains(rpc_call, "utxos")
    rep = call.type_convert(rpc_call)
    addr_response = rep.get('address')
    if addr_response != addr:
        raise AssertionError("addr missmatch: ", addr_response, addr)
    # Case 2 - known data
    rpc_call = call.nspv_listunspent(url, userpass, real_addr, 0, 0)
    call.assert_success(rpc_call)
    call.assert_contains(rpc_call, "utxos")
    rep = call.type_convert(rpc_call)
    addr_response = rep.get('address')
    if addr_response != real_addr:
        raise AssertionError("addr missmatch: ", addr_response, real_addr)
    # Case 3 - known data, isCC = 1, should not return utxos on KMD chain
    rpc_call = call.nspv_listunspent(url, userpass, real_addr, 1, 0)
    call.assert_success(rpc_call)
    call.assert_not_contains(rpc_call, "utxos")
    rep = call.type_convert(rpc_call)
    addr_response = rep.get('address')
    if addr_response != real_addr:
        raise AssertionError("addr missmatch: ", addr_response, real_addr)
    # Case 4 - fresh generated data, similar to case 1
    rpc_call = call.nspv_listunspent(url, userpass, addr, 0, 0)
    call.assert_success(rpc_call)
    call.assert_not_contains(rpc_call, "utxos")
    rep = call.type_convert(rpc_call)
    addr_response = rep.get('address')
    if addr_response != addr:
        raise AssertionError("addr missmatch: ", addr_response, addr)


    # spend call
    # Successful response should contain tx and transaction hex
    print("testing spend call")
    amount = [False, 0.0001]
    address = [False, addr_send]
    # Case 1 - false data
    rpc_call = call.nspv_spend(url, userpass, address[0], amount[0])
    call.assert_error(rpc_call)
    rpc_call = call.nspv_spend(url, userpass, address[1], amount[0])
    call.assert_error(rpc_call)
    # Case 2 - known data, not enough balance
    rpc_call = call.nspv_spend(url, userpass, address[1], amount[1])
    call.assert_error(rpc_call)
    # Case 3 - login with wif, create a valid transaction
    call.nspv_logout(url, userpass)
    call.nspv_login(url, userpass, wif_real)
    rpc_call = call.nspv_spend(url, userpass, address[1], amount[1])
    call.assert_success(rpc_call)
    call.assert_contains(rpc_call, "tx")
    call.assert_contains(rpc_call, "hex")
    # save hex for future broadcast
    rep = call.type_convert(rpc_call)
    hex_res = rep.get("hex")
    # broadcast call
    print("testing broadcast call")
    # Successful broadcasst should have equal hex broadcasted and expected
    hex = [False, "norealhexhere", hex_res]
    retcode_failed = [-1, -2, -3]
    # Cae 1 - No hex given
    rpc_call = call.nspv_broadcast(url, userpass, hex[0])
    call.assert_error(rpc_call)
    # Case 2 - Non-valid hex, failed broadcast should contain appropriate retcode
    rpc_call = call.nspv_broadcast(url, userpass, hex[1])
    call.assert_in(rpc_call, "retcode", retcode_failed)
    # Case 3 - Hex of previous transaction
    rpc_call = call.nspv_broadcast(url, userpass, hex[2])
    call.assert_success(rpc_call)
    rep = call.type_convert(rpc_call)
    broadcast_res = rep.get("broadcast")
    expected = rep.get("expected")
    if broadcast_res == expected:
        pass
    else:
        raise AssertionError("Aseert equal braodcast: ", broadcast_res, expected)
    time.sleep(1)
    # spentinfo call
    print("testing spentinfo call")
    # Successful response sould contain same txid and same vout
    # r_txids = [False, "224c0b2bd80983f44a638d6ae14aab39acc898771ebe5101dd567b13cd5fff78"]
    r_txids = [False, "67ffe0eaecd6081de04675c492a59090b573ee78955c4e8a85b8ac0be0e8e418"]
    r_vouts = [False, 1]
    # Case 1 - False data
    rpc_call = call.nspv_spentinfo(url, userpass, r_txids[0], r_vouts[0])
    call.assert_error(rpc_call)
    # Case 2 - known data
    rpc_call = call.nspv_spentinfo(url, userpass, r_txids[1], r_vouts[1])
    call.assert_success(rpc_call)
    rep = call.type_convert(rpc_call)
    txid_resp = rep.get("txid")
    if r_txids[1] != txid_resp:
        raise AssertionError("Unexpected txid: ", r_txids[1], txid_resp)
    vout_resp = rep.get("vout")
    if r_vouts[1] != vout_resp:
        raise AssertionError("Unxepected vout: ", r_vouts[1], vout_resp)
    print("all tests passed")
if __name__ == "__main__":
    main()
