# 5

## Thinking through arbitrage identification algorithm

### Scenario 1

testnet_pool_1 = "<POOL_1_ADDRESS>"  # MIALGO/ALB - ie: 1 MIALGO for 2 ALB
testnet_pool_2 = "<POOL_2_ADDRESS>"  # ALB/MIALGO - ie: 1 ALB form 2 MIALGO

1 MIALGO would give you 2 ALB which would give you 4 MIALGO back

0.5:0.5

### Scenario 2

testnet_pool_1 = "<POOL_1_ADDRESS>"  # MIALGO/ALB - ie: 1 MIALGO for 1 ALB
testnet_pool_2 = "<POOL_2_ADDRESS>"  # ALB/MIALGO - ie: 1 ALB form 2 MIALGO

1 MIALGO would give you 1 ALB which would give you 2 MIALGO back

1:0.5

### Scenario 3

testnet_pool_1 = "<POOL_1_ADDRESS>"  # MIALGO/ALB - ie: 1 MIALGO for 0.8 ALB
testnet_pool_2 = "<POOL_2_ADDRESS>"  # ALB/MIALGO - ie: 1 ALB form 2 MIALGO

1 MIALGO would give you 0.8 ALB which would give you 1.6 MIALGO back

1.25:0.5


### Scenario 4

testnet_pool_1 = "<POOL_1_ADDRESS>"  # MIALGO/ALB - ie: 1 MIALGO for 0.5 ALB
testnet_pool_2 = "<POOL_2_ADDRESS>"  # ALB/MIALGO - ie: 1 ALB form 2 MIALGO

1 MIALGO would give you 0.5 ALB which would give you 1 MIALGO back

1/2:2/1


### Scenario 5

testnet_pool_1 = "<POOL_1_ADDRESS>"  # MIALGO/ALB - ie: 1 MIALGO for 0.2 ALB
testnet_pool_2 = "<POOL_2_ADDRESS>"  # ALB/MIALGO - ie: 1 ALB form 6 MIALGO

1 MIALGO would give you 0.5 ALB which would give you 1 MIALGO back

1/.2 = 5 so reciprocal is 1/5 and any ratios above 1/5 (minus tx fees would make money)

### Summary

Take the reciprocal of the first ratio and look for ratios greater than the (reciprocal) and verify that the gains - txns fees are still profitable
