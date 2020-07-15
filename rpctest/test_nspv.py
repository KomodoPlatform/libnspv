#!/usr/bin/env python3
# Copyright (c) 2019 SuperNET developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from test_framework.nspvlib import NspvRpcCalls as NRC
import pytest
import time
import json
import os

"""
   Simple unittest based ob pytest framework for libnspv
   Make sure you have installed framework: pip3 install pytest
   Set wif to spend form and address to spend to as json in test_setup.txt file
   Default coin is ILN
   You can add any new coins to test, please set coin_params dict entry
   To run tests do: "python3 -m pytest test_nspv.py -s" from rpctest directory
"""


def setup_module():
    global addr_send, wif_real, coin, call, chain_params

    #f = open("test_setup.txt", "r")
    #test_setup = json.load(f)
    #f.close()

    # wif_real = test_setup.get("wif")
    wif_real = os.environ.get('WALL')
    addr_send = os.environ.get('ADDRESS')
    coin = os.environ.get('CHAIN')

    if not addr_send or not wif_real:
        pytest.exit("Please check test wif and address variables availability")

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
                            'tx_proof_hex': '0400008085202f8902fd49a37307311c6291c4a2d019fef867f1587bda1cf756886edef76460596b44000000006b483045022100a3883009c3cbc698d5ed507880d8097b634bd061666fd2a9c5bfcbc378771e6e02203275aa53bb2ca5561bf34f67f7bff4ba69909be24f3a5e5e5c32a34b7e873f700121022e9e79e5d87e8bd562b1a6f87ad19ee8f54f09c0e014f971608b164edb396154feffffff395ff1a8c008c69ad172963b191d3ef647fd83d0e43b63adf4c64271ddcf9835000000006a47304402206b6d7ee89ab3dfccc2b9b08f6fb78e7b6e64c8b37dcb8d30c888a1bd5ba6a6ab0220130c73a034956b65184d47378eba6a01e7e9686d3c1c89a889606b9369028d63012103c67330293d466eb61bb4cdf2c886cbe04b24b2e2bfaca2239a6d4dd6504ee69ffeffffff02988b9706000000001976a9149611ac26733deb915d4e61a8a99286c298723f6a88ac2c185c19000000001976a9141d56621b69a14ef32c71c5d2bf5970335248331888ac01c8375de43816000000000000000000000000',
                            'port': '7771',
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
                            'tx_proof_hex': '0400008085202f8901d354bc6c0168810c940da2a1dbf7b86fbd1a7af7903e2aa58e8eb3127493f3b00100000049483045022100b301101cc52a8a4e93ada52143bf2eb67a1efb8487b8631b6a3882befa0c24c9022055ba76dc2c0f0ca2e8143c3d10f12586c3ddbb80fc664e8e8f2642d2bc3f430a01ffffffff024014502e000000001976a91488b1e3638c6ba4b13c64a09111d0b93dbd5afc1f88ac6094b884d00c000023210286de5bd7831baacc55b87cdf14a1938b2f2ab905529c739c82709c2993cfeafcac00000000000000000000000000000000000000',
                            'port': '12986',
                           },
                    "HUSH": {
                             'tx_list_address': 'RCNp322uAXmNo37ipQAEjcGQgBXY9EW9yv',
                             'min_chain_height': 69951,
                             'notarization_height': '69900',
                             'prev_notarization_h': 69800,
                             'next_notarization_h': 69700,
                             'hdrs_proof_low': '66100',
                             'hdrs_proof_high': '66200',
                             'numhdrs_expected': 123,
                             'tx_proof_id': '661bae364443948a009fa7f706c3c8b7d3fa6b0b27eca185b075abbe85bbdedc',
                             'tx_spent_height': 2681,
                             'tx_proof_height': '2690',
                             'tx_proof_hex': '0400008085202f89016dff5a7406f8d831a7614386f225cb5e15449393c55817c439fe5e1d8cbe1044070000006b4830450221009616dcbe00e8ba188d0e30364da97dd277713688fc313b2ebe2635955fc7d2b602203baaabe2451193500831aecd9b51360455e68ef58be1f36d1c0fe670122e06ce01210303725d8525b6f969122faf04152653eb4bf34e10de92182263321769c334bf58ffffffff0a102700000000000023210303725d8525b6f969122faf04152653eb4bf34e10de92182263321769c334bf58ac102700000000000023210303725d8525b6f969122faf04152653eb4bf34e10de92182263321769c334bf58ac102700000000000023210303725d8525b6f969122faf04152653eb4bf34e10de92182263321769c334bf58ac102700000000000023210303725d8525b6f969122faf04152653eb4bf34e10de92182263321769c334bf58ac102700000000000023210303725d8525b6f969122faf04152653eb4bf34e10de92182263321769c334bf58ac102700000000000023210303725d8525b6f969122faf04152653eb4bf34e10de92182263321769c334bf58ac102700000000000023210303725d8525b6f969122faf04152653eb4bf34e10de92182263321769c334bf58ac102700000000000023210303725d8525b6f969122faf04152653eb4bf34e10de92182263321769c334bf58ac102700000000000023210303725d8525b6f969122faf04152653eb4bf34e10de92182263321769c334bf58ac2aa97f05000000001976a9149fcdb676cf2df71ad22124acf1294549d0509ae788ac00000000000000000000000000000000000000',
                             'port': '18031'
                            },
                    # not sure if all data below is correct
                    # hdrsproof response ref: https://gist.githubusercontent.com/pbca26/4834746f753de2e20d162cbe9019010f/raw/eebc0aa2a860655cb59f70d4bcee751fceddc1c9/nspv-hdrsproof-rick.json
                    "RICK": {
                            'tx_list_address': 'RBZ9cckqX5kUNKVD3ouZSzsqvdrmmyPg7s',
                            'min_chain_height': 481073,
                            'notarization_height': '1468000',
                            'prev_notarization_h': 481354,
                            'next_notarization_h': 481390,
                            'hdrs_proof_low': '481364',
                            'hdrs_proof_high': '481380',
                            'numhdrs_expected': 37,
                            'tx_proof_id': 'dcd9d4a23405c25f65a341319f0a860cd4ffa364510bb1180aeab57efc1315f0',
                            'tx_spent_height': 477369,
                            'tx_proof_height': '477369',
                            'tx_proof_hex': '0400008085202f89017f60812cb7637c87918b6ee3c574b104e46088f0d00c1d9067deb4076fa50005030000006b48304502210098927d1daba33455061487938796602a24c75b1a4fee8355264a821d8064f803022049b43e9d1392854022cf9db20b758c124df907504eb435074d65dc2c9f8c5d6f012102d09f2cb1693be9c0ea73bb48d45ce61805edd1c43590681b02f877206078a5b3ffffffff0400e1f505000000001976a91418f4d9ad759bc3159b405d3f690c74e45d6a851788ac00c2eb0b000000001976a91418f4d9ad759bc3159b405d3f690c74e45d6a851788aca01f791c000000001976a91418f4d9ad759bc3159b405d3f690c74e45d6a851788ac2fe85d1cfd0100001976a91490a0d8ba62c339ade97a14e81b6f531de03fdbb288ac00000000000000000000000000000000000000',
                            'port': '25435',
                           },
                    }
    userpass = "userpass"
    url = "http://127.0.0.1:" + chain_params.get(coin).get("port")
    call = NRC(url, userpass)
    call.nspv_logout()


def test_help_call():
    """ Response should contain "result": "success"
        Response should contain actual help data"""
    print('\n', "testing help call")
    rpc_call = call.nspv_help()
    if not rpc_call:
        pytest.exit("Can't connect daemon")
    call.assert_success(rpc_call)
    call.assert_contains(rpc_call, "methods")


def test_getpeerinfo_call():
    """Response should not be empty, at least one node should be in sync"""
    print('\n', "testing peerinfo call, checking peers status")
    rpc_call = call.type_convert(call.nspv_getpeerinfo())
    if not rpc_call[0]:
        raise Exception("Empty response :", rpc_call)
    call.assert_contains(rpc_call[0], "ipaddress")


def test_check_balance():
    """Check if wif given has actual balance to perform further tests"""
    print('\n', "Checking wif balance")
    call.nspv_login(wif_real)
    res = call.type_convert(call.nspv_listunspent())
    amount = res.get("balance")
    if amount > 0.1:
        pass
    else:
        pytest.exit("Not enough balance, please use another wif")


def test_getinfo_call():
    """ Response should contain "result": "success"
        Response should contain actual data"""
    print('\n', "testing getinfo call")
    rpc_call = call.nspv_getinfo()
    call.assert_success(rpc_call)
    call.assert_contains(rpc_call, "notarization")
    call.assert_contains(rpc_call, "header")


def test_hdrsproof_call():
    """ Response should be successful for case 2 and fail for others
        Response should contain actual headers"""
    print('\n', "testing hdrsproof call")
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
    print('\n', "testing notarization call")
    height = [False, chain_params.get(coin).get("notarization_height")]

    # Case 1 - False data
    rpc_call = call.nspv_notarizations(height[0])
    call.assert_error(rpc_call)

    # Case 2 - known data
    rpc_call = call.nspv_notarizations(height[1])
    call.assert_success(rpc_call)
    call.assert_contains(rpc_call, "prev")
    call.assert_contains(rpc_call, "next")


def getnewaddress_call():
    """ Get a new address, save it for latter calls"""
    print('\n', "testing getnewaddr call")
    rpc_call = call.nspv_getnewaddress()
    call.assert_contains(rpc_call, "wifprefix")
    call.assert_contains(rpc_call, "wif")
    call.assert_contains(rpc_call, "address")
    call.assert_contains(rpc_call, "pubkey")


def test_login_call():
    """"login with fresh credentials
        Response should contain address, address should be equal to generated earlier one"""
    print('\n', "testing log in call")
    global logged_address
    rpc_call = call.nspv_getnewaddress()
    rep = call.type_convert(rpc_call)
    wif = rep.get('wif')
    addr = rep.get('address')
    rpc_call = call.nspv_login(wif)
    call.assert_success(rpc_call)
    call.assert_contains(rpc_call, "status")
    call.assert_contains(rpc_call, "address")
    rep = call.type_convert(rpc_call)
    logged_address = rep.get('address')
    if logged_address != addr:
        raise AssertionError("addr missmatch: ", addr, logged_address)


def test_listtransactions_call():
    """"Successful response should [not] contain txids and same address as requested
        Case 1 - False data, user is logged in - should not print txids for new address"""
    print('\n', "testing listtransactions call")
    call.nspv_logout()
    real_addr = chain_params.get(coin).get("tx_list_address")

    # Case 1 - False Data
    rpc_call = call.nspv_listtransactions(False, False, False)
    call.assert_success(rpc_call)
    call.assert_not_contains(rpc_call, "txids")
    rep = call.type_convert(rpc_call)
    addr_response = rep.get('address')
    if addr_response != logged_address:
        raise AssertionError("addr missmatch: ", addr_response, logged_address)

    # Case 2 - known data
    rpc_call = call.nspv_listtransactions(real_addr, 0, 1)
    call.assert_success(rpc_call)
    call.assert_contains(rpc_call, "txids")
    rep = call.type_convert(rpc_call)
    addr_response = rep.get('address')
    if addr_response != real_addr:
        raise AssertionError("addr missmatch: ", addr_response, real_addr)

    # Case 3 - known data, isCC = 1
    rpc_call = call.nspv_listtransactions(real_addr, 1, 1)
    call.assert_success(rpc_call)
    call.assert_not_contains(rpc_call, "txids")
    rep = call.type_convert(rpc_call)
    addr_response = rep.get('address')
    if addr_response != real_addr:
        raise AssertionError("addr missmatch: ", addr_response, real_addr)


def test_litunspent_call():
    """ Successful response should [not] contain utxos and same address as requested"""
    print('\n', "testing listunspent call")
    call.nspv_logout()
    real_addr = chain_params.get(coin).get("tx_list_address")

    # Case 1 - False dataf
    rpc_call = call.nspv_listunspent(False, False, False)
    call.assert_success(rpc_call)
    call.assert_not_contains(rpc_call, "utxos")
    rep = call.type_convert(rpc_call)
    addr_response = rep.get('address')
    if addr_response != logged_address:
        raise AssertionError("addr missmatch: ", addr_response, logged_address)

    # Case 2 - known data
    rpc_call = call.nspv_listunspent(real_addr, 0, 0)
    call.assert_success(rpc_call)
    call.assert_contains(rpc_call, "utxos")
    rep = call.type_convert(rpc_call)
    addr_response = rep.get('address')
    if addr_response != real_addr:
        raise AssertionError("addr missmatch: ", addr_response, real_addr)

    # Case 3 - known data, isCC = 1, should not return utxos
    rpc_call = call.nspv_listunspent(real_addr, 1, 0)
    call.assert_success(rpc_call)
    call.assert_not_contains(rpc_call, "utxos")
    rep = call.type_convert(rpc_call)
    addr_response = rep.get('address')
    if addr_response != real_addr:
        raise AssertionError("addr missmatch: ", addr_response, real_addr)


def test_spend_call():
    """Successful response should contain tx and transaction hex"""
    print('\n', "testing spend call")
    amount = [False, 0.1]
    address = [False, addr_send]

    # Case 1 - false data
    rpc_call = call.nspv_spend(address[0], amount[0])
    call.assert_error(rpc_call)
    rpc_call = call.nspv_spend(address[1], amount[0])
    call.assert_error(rpc_call)

    # Case 2 - known data, no legged in user
    rpc_call = call.nspv_spend(address[1], amount[1])
    call.assert_error(rpc_call)

    # Case 3 - login with wif, create a valid transaction
    call.nspv_logout()
    call.nspv_login(wif_real)
    rpc_call = call.nspv_spend(address[1], amount[1])
    call.assert_success(rpc_call)
    call.assert_contains(rpc_call, "tx")
    call.assert_contains(rpc_call, "hex")


def test_broadcast_call():
    """Successful broadcasst should have equal hex broadcasted and expected"""
    print('\n', "testing broadcast call")
    call.nspv_logout()
    call.nspv_login(wif_real)
    rpc_call = call.nspv_spend(addr_send, 0.1)
    rep = call.type_convert(rpc_call)
    hex_res = rep.get("hex")
    hex = [False, "norealhexhere", hex_res]
    retcode_failed = [-1, -2, -3]

    # Cae 1 - No hex given
    rpc_call = call.nspv_broadcast(hex[0])
    call.assert_error(rpc_call)

    # Case 2 - Non-valid hex, failed broadcast should contain appropriate retcode
    rpc_call = call.nspv_broadcast(hex[1])
    call.assert_in(rpc_call, "retcode", retcode_failed)

    # Case 3 - Hex of previous transaction
    rpc_call = call.nspv_broadcast(hex[2])
    call.assert_success(rpc_call)
    rep = call.type_convert(rpc_call)
    broadcast_res = rep.get("broadcast")
    expected = rep.get("expected")
    if broadcast_res == expected:
        pass
    else:
        raise AssertionError("Assert equal broadcast: ", broadcast_res, expected)


def test_mempool_call():
    """ Response should contain txids"""
    print('\n', "testing mempool call")
    rpc_call = call.nspv_mempool()
    call.assert_success(rpc_call)
    # call.assert_contains(rpc_call, "txids") - mempool() response not always contains "txids" key, even on success


def test_spentinfo_call():
    """Successful response sould contain same txid and same vout"""
    print('\n', "testing spentinfo call")
    r_txids = [False, chain_params.get(coin).get("tx_proof_id")]
    r_vouts = [False, 1]

    # Case 1 - False data
    rpc_call = call.nspv_spentinfo(r_txids[0], r_vouts[0])
    call.assert_error(rpc_call)

    # Case 2 - known data
    rpc_call = call.nspv_spentinfo(r_txids[1], r_vouts[1])
    call.assert_success(rpc_call)
    rep = call.type_convert(rpc_call)
    txid_resp = rep.get("txid")
    if r_txids[1] != txid_resp:
        raise AssertionError("Unexpected txid: ", r_txids[1], txid_resp)
    vout_resp = rep.get("vout")
    if r_vouts[1] != vout_resp:
        raise AssertionError("Unxepected vout: ", r_vouts[1], vout_resp)


def test_faucetinfo():
    """Not implemented call yet"""
    return True


def test_gettransaction():
    print('\n', "testing gettransaction call")
    rpc_call = call.nspv_gettransaction(chain_params.get(coin).get("tx_proof_id"))
    call.assert_contains(rpc_call, "hex")
    rep = call.type_convert(rpc_call)
    rawhex = rep.get("hex")
    if chain_params.get(coin).get("tx_proof_hex") == rawhex:
        pass
    else:
        raise AssertionError("Aseert equal gettransaction: ", rawhex, chain_params.get(coin).get("tx_proof_hex"))

def test_autologout():
    """Wif should expeire in 777 seconds"""
    print('\n', "testing auto logout")
    rpc_call = call.nspv_getnewaddress()
    rep = call.type_convert(rpc_call)
    wif = rep.get('wif')
    rpc_call = call.nspv_login(wif)
    call.assert_success(rpc_call)
    time.sleep(778)
    rpc_call = call.nspv_spend(addr_send, 0.1)
    call.assert_error(rpc_call)


def test_stop():
    """Send funds to reset utxo amount in wallet
       Stop nspv process after tests"""
    print('\n', "Resending funds")
    maxfee = 0.01
    call.nspv_login(wif_real)
    res = call.type_convert(call.nspv_listunspent())
    amount = res.get("balance") - maxfee
    res = call.type_convert(call.nspv_spend(addr_send, amount))
    hexs = res.get("hex")
    call.nspv_broadcast(hexs)
    print('\n', "stopping nspv process")
    rpc_call = call.nspv_stop()
    call.assert_success(rpc_call)
    print('\n', "all tests are finished")
