package main

import (
	"context"
	"math/big"
	"time"

	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/ethclient"
)

func CollectEthBalance(selectedAddresses []string, client *ethclient.Client) (map[string]float64, map[string]map[string]float64, error) {
	whalesIndividualBalance := make(map[string]map[string]float64)
	whalesTotalBalance := make(map[string]float64)
	startdate := time.Date(2018, time.January, 1, 0, 0, 0, 0, time.UTC)
	enddate := time.Date(2023, time.January, 1, 0, 0, 0, 0, time.UTC)
	range_ := make([]time.Time, 0)
	for d := startdate; d.Before(enddate); d = d.AddDate(0, 0, 1) {
		range_ = append(range_, d)
	}

	for _, address := range selectedAddresses {
		whalesIndividualBalance[address] = make(map[string]float64)
		for _, date := range range_ {
			dateString := date.Format("2006/01/02")
			whalesIndividualBalance[address][dateString] = 0
		}
	}

	for _, date := range range_ {
		dateString := date.Format("2006/01/02")
		whalesTotalBalance[dateString] = 0
	}

	for _, date := range range_ {
		block, err := client.BlockByDate(context.Background(), date)
		if err != nil {
			return nil, nil, err
		}
		blockNumber := block.Number()
		dateString := date.Format("2006/01/02")
		for _, address := range selectedAddresses {
			address := common.HexToAddress(address)
			balance, err := client.BalanceAt(context.Background(), address, blockNumber)
			if err != nil {
				return nil, nil, err
			}
			ethBalance := new(big.Float).Quo(new(big.Float).SetInt(balance), big.NewFloat(params.Ether))
			whalesIndividualBalance[address.String()][dateString] = ethBalance.Float64()
			whalesTotalBalance[dateString] += ethBalance.Float64()
		}
	}

	return whalesTotalBalance, whalesIndividualBalance, nil
}
