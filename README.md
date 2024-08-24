# Malicious Validators Analysis

## Overview

	•	Total Validators Identified: 241
	•	Total Amount of Stake: 8,575,767 SOL
	•	Validators with Stake >15k: 156
	•	Validators with SFDP: 144

## Methodology Summary
1. [Collect all txns with a known sandwicher as the signer](https://github.com/a-guard/malicious-validators/blob/48ef59afa8fa3ec7e61c28cee9e41a489a984714/find_sigs.py#L12C38-L12C82) (Ec9xymGeMuURLQfpMsMPkEwy5ktAiQSaFSjF5oJ3kERa)
2. [filter out txns that make a tip to any jito tip collector](https://github.com/a-guard/malicious-validators/blob/48ef59afa8fa3ec7e61c28cee9e41a489a984714/filter_sigs.py#L45C5-L51C39)
3. [filter out txns that aren’t raydium trades](https://github.com/a-guard/malicious-validators/blob/48ef59afa8fa3ec7e61c28cee9e41a489a984714/filter_sigs.py#L45C5-L51C39)
4. [group txns that are in the same slot and have a net positive post balance on the same trading pair](https://github.com/a-guard/malicious-validators/blob/48ef59afa8fa3ec7e61c28cee9e41a489a984714/filter_sigs.py#L63C2-L70C58)
5. [group identified sandwich txns and leader slots against leader schedule.](https://github.com/a-guard/malicious-validators/blob/main/find_by_stake_authority.py)

Some of the txns might not be sandwiches but upon spot checking [the sandwich groupings](https://github.com/a-guard/malicious-validators/blob/main/data/filtered_sandwitches.json) it's clear that most of these are sandwich txns. 

One could also spot check the hashes to see if they are a part of any bundles at [https://explorer.jito.wtf/](https://explorer.jito.wtf/)

## Why Are Sandwich Attacks Harmful?

Sandwich attacks are a type of front-running attack that can cause significant harm in decentralized finance (DeFi) environments, particularly on automated market makers (AMMs) like Raydium. Here’s why they are detrimental:

1. Increased Costs for Users
In a sandwich attack, a malicious actor observes a pending transaction and strategically places their own transactions before and after the target transaction. This manipulation can lead to unfavorable price changes for the original transaction. As a result, the victim ends up buying assets at a higher price or selling them at a lower price than expected, effectively losing money to the attacker.
2. Market Manipulation
Sandwich attacks distort the market by artificially inflating or deflating asset prices. This manipulation reduces the transparency and fairness of the market, making it harder for legitimate users to trade at fair prices.
3. Erosion of Trust in DeFi Platforms
The prevalence of sandwich attacks can undermine trust in DeFi platforms. When users repeatedly experience losses due to these attacks, they may lose confidence in the security and integrity of the platform, leading to reduced participation and liquidity.
4. Undermining the Efficiency of the Ecosystem
By exploiting the system for personal gain, attackers contribute nothing to the ecosystem and instead extract value from it. This can slow down the growth and adoption of decentralized finance as users become wary of engaging with vulnerable platforms.

## Conclusion

Sandwich attacks are harmful because they exploit the decentralized nature of DeFi platforms, leading to financial losses for individual users and overall harm to the ecosystem. Identifying and mitigating these attacks is crucial for maintaining a fair, transparent, and trustworthy financial environment.
