//
//  RootViewController.h
//  sohukan
//
//  Created by riven on 12-1-15.
//  Copyright 2012年 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>

@class ListViewController;
@interface RootViewController : UITableViewController {
    ListViewController *listViewController;
    NSArray *controllers;
}
@property(nonatomic, retain)NSArray *controllers;
//@property(nonatomic, retain)ListViewController *listViewController;

@end