TL:DR on the methdology:
1. [Collect all txns with a known sandwicher as the signer](https://github.com/a-guard/malicious-validators/blob/48ef59afa8fa3ec7e61c28cee9e41a489a984714/find_sigs.py#L12C38-L12C82) (Ec9xymGeMuURLQfpMsMPkEwy5ktAiQSaFSjF5oJ3kERa)
2. [filter out txns that make a tip to any jito tip collector](https://github.com/a-guard/malicious-validators/blob/48ef59afa8fa3ec7e61c28cee9e41a489a984714/filter_sigs.py#L45C5-L51C39)
3. [filter out txns that aren’t raydium trades](https://github.com/a-guard/malicious-validators/blob/48ef59afa8fa3ec7e61c28cee9e41a489a984714/filter_sigs.py#L45C5-L51C39)
4. [group txns that are in the same slot and have a net positive post balance on the same trading pair](https://github.com/a-guard/malicious-validators/blob/48ef59afa8fa3ec7e61c28cee9e41a489a984714/filter_sigs.py#L63C2-L70C58)
5. [group identified sandwich txns and leader slots against leader schedule.](https://github.com/a-guard/malicious-validators/blob/main/find_by_stake_authority.py)

Some of the txns might not be sandwiches but upon spot checking [the sandwich groupings](https://github.com/a-guard/malicious-validators/blob/main/data/filtered_sandwitches.json) it's clear that most of these are sandwich txns. 

One could also spot check the hashes to see if they are a part of any bundles at [https://explorer.jito.wtf/](https://explorer.jito.wtf/)