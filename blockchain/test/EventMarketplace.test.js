const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("EventMarketplace", function () {
    let EventToken;
    let EventNFT;
    let EventMarketplace;
    let eventToken;
    let eventNFT;
    let eventMarketplace;
    let owner;
    let buyer;
    let seller;
    let ticketPriceList;
    let ticketSupplyList;

    beforeEach(async function () {
        [owner, buyer, seller] = await ethers.getSigners();

        // Deploy EventToken
        EventToken = await ethers.getContractFactory("EventToken");
        eventToken = await EventToken.deploy();
        await eventToken.deployed();

        // Setup ticket prices and supplies
        ticketPriceList = [
            ethers.utils.parseEther("0.1"), // Level 0
            ethers.utils.parseEther("0.2"), // Level 1
            ethers.utils.parseEther("0.3")  // Level 2
        ];
        ticketSupplyList = [100, 50, 25]; // Supply for each level

        // Deploy EventNFT
        EventNFT = await ethers.getContractFactory("EventNFT");
        eventNFT = await EventNFT.deploy(
            "Test Festival",
            "TEST",
            2, // maxTicketLevel
            ticketPriceList,
            ticketSupplyList,
            owner.address
        );
        await eventNFT.deployed();

        // Deploy EventMarketplace
        EventMarketplace = await ethers.getContractFactory("EventMarketplace");
        eventMarketplace = await EventMarketplace.deploy(eventToken.address, eventNFT.address);
        await eventMarketplace.deployed();

        // Mint some tokens to buyer for testing
        await eventToken.mint(buyer.address, ethers.utils.parseEther("1000"));
        await eventToken.mint(seller.address, ethers.utils.parseEther("1000"));
    });

    describe("Primary Market Purchase", function () {
        it("should allow purchase of ticket from primary market", async function () {
            const ticketLevel = 0;
            const ticketPrice = await eventNFT.getTicketPrice(ticketLevel);

            // Approve marketplace to spend tokens
            await eventToken.connect(buyer).approve(eventMarketplace.address, ticketPrice);

            // Purchase ticket
            await eventMarketplace.connect(buyer).purchaseTicket(ticketLevel, buyer.address);

            // Verify ticket ownership
            const ticketId = 1; // First ticket
            expect(await eventNFT.ownerOf(ticketId)).to.equal(buyer.address);
        });

        it("should fail if buyer has insufficient tokens", async function () {
            const ticketLevel = 0;
            const ticketPrice = await eventNFT.getTicketPrice(ticketLevel);

            // Set buyer balance to 0
            await eventToken.connect(buyer).burn(await eventToken.balanceOf(buyer.address));

            // Attempt to purchase ticket
            await expect(
                eventMarketplace.connect(buyer).purchaseTicket(ticketLevel, buyer.address)
            ).to.be.reverted;
        });
    });

    describe("Secondary Market Purchase", function () {
        beforeEach(async function () {
            // First purchase a ticket through primary market
            const ticketLevel = 0;
            const ticketPrice = await eventNFT.getTicketPrice(ticketLevel);
            await eventToken.connect(seller).approve(eventMarketplace.address, ticketPrice);
            await eventMarketplace.connect(seller).purchaseTicket(ticketLevel, seller.address);

            // Set ticket for sale in secondary market
            const ticketId = 1;
            const sellingPrice = ethers.utils.parseEther("0.15"); // 150% of original price
            await eventNFT.connect(seller).setSaleDetails(ticketId, sellingPrice, eventMarketplace.address);
        });

        it("should allow purchase of ticket from secondary market", async function () {
            const ticketId = 1;
            const sellingPrice = await eventNFT.getSellingPrice(ticketId);

            // Approve marketplace to spend tokens
            await eventToken.connect(buyer).approve(eventMarketplace.address, sellingPrice);

            // Purchase ticket
            await eventMarketplace.connect(buyer).secondaryPurchase(ticketId, buyer.address);

            // Verify ticket ownership
            expect(await eventNFT.ownerOf(ticketId)).to.equal(buyer.address);
        });

        it("should fail if selling price exceeds 110% of purchase price", async function () {
            const ticketId = 1;
            const originalPrice = await eventNFT.getTicketPrice(0);
            const invalidSellingPrice = originalPrice.mul(120).div(100); // 120% of original price

            // Attempt to set invalid selling price
            await expect(
                eventNFT.connect(seller).setSaleDetails(ticketId, invalidSellingPrice, eventMarketplace.address)
            ).to.be.revertedWith("Re-selling price is more than 110%");
        });

        it("should fail if buyer has insufficient tokens", async function () {
            const ticketId = 1;
            const sellingPrice = await eventNFT.getSellingPrice(ticketId);

            // Set buyer balance to 0
            await eventToken.connect(buyer).burn(await eventToken.balanceOf(buyer.address));

            // Attempt to purchase ticket
            await expect(
                eventMarketplace.connect(buyer).secondaryPurchase(ticketId, buyer.address)
            ).to.be.reverted;
        });
    });
}); 