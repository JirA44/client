
---
// FILE: src/api/assets.js
import { get } from 'svelte/store'
import { ethers } from 'ethers'
import { CURRENCY_DECIMALS } from '@lib/config'
import { updateBalances } from '@lib/connect'
import { getContract } from '@lib/contracts'
import { formatUnits, parseUnits } from '@lib/formatters'
import { address, provider, balances, selectedAsset, allowances } from '@lib/stores'
import { getAssets } from '@lib/utils'
import { showToast, showError } from '@lib/ui'

async function getBalanceOf(asset) {
	const _address = get(address);
	if (!_address) return 0;
	let balance, decimals;
	if (asset == 'ETH') {
		balance = await get(provider).getBalance(_address);
	} else {
		const contract = await getContract(asset);
		decimals = CURRENCY_DECIMALS[asset];
		balance = await contract.balanceOf(_address);
	}
	return formatUnits(balance, decimals || 18);
}

export async function getUserAssetBalances(assets) {
	// console.log('getUserAssetBalances', assets);
	if (!assets) assets = getAssets();
	for (const asset of assets) {
		let balance = await getBalanceOf(asset);
		balances.update((bls) => {
			bls[asset] = balance;
			return bls;
		});
	}
	//